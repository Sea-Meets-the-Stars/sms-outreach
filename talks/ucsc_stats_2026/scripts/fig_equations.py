"""Created by JXP and Claude.

Render the equations for the UCSC Statistics talk (2026) as PNGs with
matplotlib mathtext (no LaTeX install needed).  One function per equation;
``main`` writes all eight into ``talks/ucsc_stats_2026/figures/``.

Each image is drawn at the physical width of the slide cell it will occupy
(HALF 4.4", SIDE 6.1", FULL 9.0") so the font sizes below are what the
audience sees: equations 18-22 pt (a few unavoidably wide lines shrink to
fit the cell and the script prints the effective size), small annotation
labels 14 pt.  The figures are made of ``fig.text`` only (no axes); lines
are stacked top to bottom using the measured extent of the previous line,
and a white hairline across the full width pins the tight bounding box to
the cell width.  Positions are kept in figure-fraction coordinates because
``bbox_inches="tight"`` re-maps ``transFigure`` but not ``dpi_scale_trans``.

Run from the repo root:

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_equations.py

Outputs: eq_*.png (black on opaque white, dpi 220) and the manifest entries
in MANIFEST (a scratch sources.json, merged into figures/sources.json later).
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from sms_outreach.slides.style import apply_style, DPI

OUT_DIR = REPO / "talks" / "ucsc_stats_2026" / "figures"
MANIFEST = OUT_DIR / "sources.json"
SOURCE = "Equation rendered by J. X. Prochaska & Claude (matplotlib mathtext)"

HALF, SIDE, FULL = 4.4, 6.1, 9.0       # cell widths (inches)
EQ, EQ_SMALL, LABEL = 22, 20, 14       # font sizes (pt)
PAD = 0.05                             # bbox pad (inches)
MARGIN = 0.02                          # side margin inside the cell (inches)


# ----------------------------------------------------------------------------
# Layout helper.  All public positions are in inches from the figure's
# bottom-left; the figure is made tall and trimmed by bbox_inches="tight".
# ----------------------------------------------------------------------------
class Stack:
    """Created by JXP and Claude. Stack text lines top-down on a blank
    figure of the given width.  ``add`` places one line below the previous
    one (shrinking it to the cell width if needed); ``hstack`` places pieces
    left to right on one line and returns their x-centers so ``labels`` can
    put words under the terms; ``box`` frames a line; ``save`` writes the
    PNG and the manifest entry."""

    def __init__(self, width, height=4.0):
        self.W, self.H = width, height
        self.fig = plt.figure(figsize=(width, height), dpi=DPI)
        self.fig.patch.set_facecolor("white")
        self.renderer = self.fig.canvas.get_renderer()
        self.y = height - 0.05                 # top edge of the next line
        # white hairline across the full width so the tight bbox keeps it
        self.fig.add_artist(Line2D([0, 1], [self.y / height] * 2,
                                   transform=self.fig.transFigure,
                                   color="white", lw=0.3))

    # -- geometry -------------------------------------------------------
    def _extent(self, t):
        """(x0, y0, x1, y1) of a Text in inches."""
        bb = t.get_window_extent(self.renderer)
        return (bb.x0 / DPI, bb.y0 / DPI, bb.x1 / DPI, bb.y1 / DPI)

    def _text(self, x, y, s, size, ha, va="top"):
        return self.fig.text(x / self.W, y / self.H, s, fontsize=size, ha=ha,
                             va=va, transform=self.fig.transFigure,
                             color="black")

    def _set_x(self, t, x):
        t.set_x(x / self.W)

    # -- lines ------------------------------------------------------------
    def add(self, s, size=EQ, ha="center", x=None, gap=0.10):
        """Add one line; returns the Text artist."""
        if x is None:
            x = {"center": self.W / 2, "left": MARGIN, "right": self.W - MARGIN}[ha]
        t = self._text(x, self.y, s, size, ha)
        x0, y0, x1, y1 = self._extent(t)
        avail = self.W - 2 * MARGIN - (x - MARGIN if ha == "left" else 0.0)
        if x1 - x0 > avail:                     # shrink to fit the cell
            new = size * avail / (x1 - x0)
            print(f"  shrink {size} -> {new:.1f} pt: {s[:40]}")
            t.set_fontsize(new)
            x0, y0, x1, y1 = self._extent(t)
        self.y = y0 - gap
        return t

    def hstack(self, pieces, size=EQ, sep=0.06, gap=0.10):
        """Place pieces (strings) left to right on a common baseline,
        centered as a group (shrunk to fit the cell if needed).
        Returns [(x_center, x_left, x_right)]."""
        def place(size):
            texts, x = [], 0.0
            for s in pieces:       # baseline at self.y, then drop the row so
                t = self._text(x, self.y, s, size, "left", va="baseline")
                texts.append(t)    # its tallest piece starts at self.y
                x = self._extent(t)[2] + sep
            top = max(self._extent(t)[3] for t in texts)
            for t in texts:
                t.set_y((self.y - (top - self.y)) / self.H)
            return texts, x - sep
        texts, total = place(size)
        avail = self.W - 2 * MARGIN
        if total > avail:
            new = size * avail / total
            print(f"  shrink {size} -> {new:.1f} pt: {pieces[0][:30]}...")
            for t in texts:
                t.remove()
            texts, total = place(new)
        shift = (self.W - total) / 2
        centers, ymin = [], self.y
        for t in texts:
            self._set_x(t, t.get_position()[0] * self.W + shift)
            x0, y0, x1, y1 = self._extent(t)
            centers.append(((x0 + x1) / 2, x0, x1))
            ymin = min(ymin, y0)
        self.y = ymin - gap
        return centers

    def labels(self, xs, words, size=LABEL, gap=0.10):
        """Small word labels centered at the given x positions ('\\n'
        allowed); each is nudged back inside the cell if it sticks out."""
        ymin = self.y
        for xc, w in zip(xs, words):
            t = self._text(xc, self.y, w, size, "center")
            x0, y0, x1, y1 = self._extent(t)
            if x0 < MARGIN:
                self._set_x(t, xc + MARGIN - x0)
            elif x1 > self.W - MARGIN:
                self._set_x(t, xc - (x1 - (self.W - MARGIN)))
            ymin = min(ymin, self._extent(t)[1])
        self.y = ymin - gap

    def box(self, t, pad=0.07):
        """Draw a rectangle around a Text artist."""
        x0, y0, x1, y1 = self._extent(t)
        self.fig.add_artist(Rectangle(((x0 - pad) / self.W, (y0 - pad) / self.H),
                                      (x1 - x0 + 2 * pad) / self.W,
                                      (y1 - y0 + 2 * pad) / self.H,
                                      transform=self.fig.transFigure,
                                      fill=False, ec="black", lw=1.2))
        self.y = min(self.y, y0 - pad - 0.10)

    # -- output -----------------------------------------------------------
    def save(self, name, slide):
        """Write the PNG (tight bbox, opaque white) and the manifest entry."""
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / name
        self.fig.savefig(out, dpi=DPI, bbox_inches="tight", pad_inches=PAD,
                         facecolor="white")
        plt.close(self.fig)
        Image.open(out).convert("RGB").save(out)   # drop the alpha channel
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
        entry = manifest.get(name, {})
        entry.update({"slide": slide, "source": SOURCE, "origin": "generated"})
        manifest[name] = entry
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {out}")
        return out


# ----------------------------------------------------------------------------
# The equations
# ----------------------------------------------------------------------------
def eq_dm_sum():
    """DM = DM_MW + DM_cosmic(z) + DM_host/(1+z), with word labels under the terms."""
    st = Stack(HALF)
    xs = st.hstack([r"$\mathrm{DM} =$",
                    r"$\mathrm{DM_{MW}}$",
                    r"$+\ \mathrm{DM_{cosmic}}(z)$",
                    r"$+\ \dfrac{\mathrm{DM_{host}}}{1+z}$"], size=EQ, sep=0.05, gap=0.06)
    # the three physical terms are pieces 1..3 (the '+' belongs to the term,
    # so nudge the label center a little to the right of the piece center)
    st.labels([xs[1][0], xs[2][0] + 0.10, xs[3][0] + 0.12],
              ["Galactic\nmodel",
               "the signal: skewed,\nscatter " + r"$\propto F/\sqrt{z}$",
               "lognormal\n" + r"$(\mu, \sigma)$"], size=13)
    return st.save("eq_dm_sum.png", "Dispersion measure")


def eq_lambda():
    """Rate density as a product of five factors, labelled underneath
    (broken into two lines so it reads at 20 pt in a HALF cell)."""
    st = Stack(HALF)
    xs = st.hstack([r"$\lambda_s(z, \mathrm{DM}\,|\,\theta) =$",
                    r"$C$",
                    r"$\cdot\ \dfrac{dV}{dz}$",
                    r"$\cdot\ \Phi(z)^{n_{\rm sfr}}$"], size=EQ_SMALL, gap=0.06)
    st.labels([xs[1][0], xs[2][0] + 0.08, xs[3][0] + 0.08],
              ["rate", "volume", "source\nevolution"], gap=0.14)
    xs2 = st.hstack([r"$\cdot\ p(\mathrm{DM}\,|\,z)$",
                     r"$\cdot\ P_s(\mathrm{det}\,|\,z, \mathrm{DM}, \theta)$"],
                    size=EQ_SMALL, gap=0.06)
    st.labels([xs2[0][0] + 0.08, xs2[1][0] + 0.08],
              ["DM given z",
               "selection: beam, threshold,\nenergy function " + r"$(\gamma, E_{\max})$"])
    return st.save("eq_lambda.png", "Population modeling: the model")


def eq_lnL_frb():
    """Extended Poisson likelihood for the FRB population model."""
    st = Stack(SIDE, height=5.5)
    # the bracket spans two lines: \left[ ... \right. on the first,
    # \left. ... \right] on the second, so both delimiters are full height
    st.add(r"$\ln L(\theta) = \sum_s \left[\ \sum_{i\,\in\,\mathrm{localized}} "
           r"\ln\dfrac{\lambda_s(z_i, \mathrm{DM}_i)}{\Lambda_s} \right.$", size=EQ_SMALL,
           ha="left", gap=0.08)
    st.add(r"$\left. + \sum_{j\,\in\,\mathrm{DM\ only}} "
           r"\ln\dfrac{\int \lambda_s(z, \mathrm{DM}_j)\,dz}{\Lambda_s}\ \right]$",
           size=EQ_SMALL, ha="left", x=1.35, gap=0.10)
    st.add(r"$+ \sum_s \ln \mathrm{Poisson}(N_s\,|\,\Lambda_s) "
           r"+ \sum_{\rm bursts} \ln p(S/N)$", size=EQ_SMALL, ha="left", x=0.6,
           gap=0.08)
    st.add("+ repeater terms", size=EQ_SMALL, ha="left", x=0.6, gap=0.18)
    st.add(r"$\Lambda_s = \iint \lambda_s(z, \mathrm{DM}\,|\,\theta)\,dz\,d\mathrm{DM}$",
           size=EQ_SMALL, ha="left", gap=0.06)
    st.add("(the overall rate " + r"$C$" + " is profiled out)", size=LABEL,
           ha="left", x=0.6)
    return st.save("eq_lnL_frb.png", "Population modeling: the likelihood")


def eq_path():
    """PATH host association (Aggarwal et al. 2021)."""
    st = Stack(HALF, height=5.0)
    st.add(r"$P(O_i\,|\,x) = \dfrac{P(O_i)\,p(x\,|\,O_i)}{p(x)}$", gap=0.08)
    st.add(r"$p(x) = \sum_j P(O_j)\,p(x\,|\,O_j) + P(U)\,p(x\,|\,U)$",
           size=EQ_SMALL, gap=0.10)
    st.add(r"$P(O_i) \propto$" + " prior from galaxy magnitude " + r"$m_i$",
           size=LABEL, gap=0.03)
    st.add("(number counts);   " + r"$P(U)$" + ": no host seen", size=LABEL,
           gap=0.14)
    st.add(r"$p(x\,|\,O_i) = \int p(x\,|\,\omega)\,p(\omega\,|\,O_i)\,d\omega$",
           size=EQ_SMALL, gap=0.06)
    st.add("(offset distribution " + r"$\otimes$" + " localization error)",
           size=LABEL)
    return st.save("eq_path.png", "PATH")


def eq_gordon():
    """Forward model of Gordon et al. (1988); last line boxed."""
    st = Stack(HALF, height=5.0)
    st.add(r"$u = \dfrac{b_b}{a + b_b}$", gap=0.10)
    st.add(r"$r_{rs} = G_1\,u + G_2\,u^2$", size=EQ_SMALL, gap=0.06)
    st.add(r"$G_1 = 0.0949,\quad G_2 = 0.0794$", size=16, gap=0.10)
    st.add(r"$R_{rs} = \dfrac{0.52\,r_{rs}}{1 - 1.7\,r_{rs}}$", size=EQ_SMALL, gap=0.18)
    t = st.add(r"$R_{rs} = f\left(\dfrac{b_b}{a}\right)$", size=EQ)
    st.box(t)
    return st.save("eq_gordon.png", "The forward model")


def eq_iop_model():
    """Nested IOP parameterization for a(lambda) and b_b(lambda)."""
    # one equation per line (B7): the sum of parts first, then each part
    st = Stack(HALF, height=5.0)
    st.add(r"$a(\lambda) = a_w(\lambda) + a_{dg}(\lambda) + a_{ph}(\lambda)$",
           size=EQ_SMALL, ha="left", gap=0.10)
    st.add(r"$a_{dg}(\lambda) = A_{dg}\,e^{-S_{dg}(\lambda - 400)}$",
           size=EQ_SMALL, ha="left", x=0.4, gap=0.08)
    st.add(r"$a_{ph}(\lambda) = A_{ph}\,a^{*}_{ph}(\lambda)$" + "   (a template)",
           size=EQ_SMALL, ha="left", x=0.4, gap=0.16)
    st.add(r"$b_b(\lambda) = b_{b,w}(\lambda) + B_{nw}\,(\lambda/600)^{\beta}$",
           size=EQ_SMALL, ha="left", gap=0.16)
    st.add("water terms known;  2–5 free parameters:", size=LABEL, ha="left",
           gap=0.03)
    st.add(r"$A_{dg},\ S_{dg},\ A_{ph},\ B_{nw},\ \beta$", size=LABEL, ha="left",
           x=0.4)
    return st.save("eq_iop_model.png", "The forward model")


def eq_lnL_gauss():
    """Gaussian log-likelihood for the R_rs fit plus the priors."""
    st = Stack(HALF)
    st.add(r"$\ln L(\theta) = -\dfrac{1}{2}\sum_\lambda "
           r"\dfrac{[R_{rs,\mathrm{obs}}(\lambda) - R_{rs,\mathrm{model}}(\lambda;\theta)]^2}"
           r"{\sigma^2(\lambda)}$", size=18, gap=0.14)
    st.add("priors: log-uniform amplitudes;", size=LABEL, ha="left", gap=0.03)
    st.add(r"$S_{dg} \sim U[0.01, 0.02]\ \mathrm{nm}^{-1}$" + ";   "
           + r"$\beta \sim U[0, 2]$", size=LABEL, ha="left", x=0.4)
    return st.save("eq_lnL_gauss.png", "Standard MCMC")


def eq_bic():
    """BIC and the Delta-BIC used to compare nested models."""
    st = Stack(HALF)
    st.add(r"$\mathrm{BIC} = k \ln n - 2 \ln L_{\max}$", gap=0.08)
    st.add(r"$\Delta\mathrm{BIC}$" + " between nested models (" + r"$k = 2 \ldots 5$" + ")",
           size=18, gap=0.12)
    st.add("from a Levenberg–Marquardt best fit,", size=LABEL, gap=0.02)
    st.add("not from the posterior", size=LABEL)
    return st.save("eq_bic.png", "(spare)")


def main():
    apply_style()
    plt.rcParams["mathtext.fontset"] = "dejavusans"
    plt.rcParams["axes.grid"] = False
    for fn in (eq_dm_sum, eq_lambda, eq_lnL_frb, eq_path, eq_gordon,
               eq_iop_model, eq_lnL_gauss, eq_bic):
        fn()
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
