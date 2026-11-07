"""Tiny dependency-free PDF writer.

Used for the auto-generated service brochure (the 'Brochure' button on every service card)
when no PDF has been uploaded for that service in the admin panel.
It writes a real text PDF (A4, Helvetica) with word wrapping and page breaks.
"""
import datetime

# Helvetica character widths (1/1000 em) for ASCII 32..126
_W = [
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
    1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
    333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
    556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
]

PURPLE = (0.486, 0.227, 0.929)
DARK = (0.09, 0.10, 0.16)
GRAY = (0.38, 0.42, 0.50)
WHITE = (1, 1, 1)
SOFT = (0.93, 0.91, 0.99)

_REPLACE = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ", "→": "->",
}


def _clean(text):
    text = str(text or "")
    for a, b in _REPLACE.items():
        text = text.replace(a, b)
    return text.replace("\r", "")


def _esc(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class _Pdf:
    PAGE_W, PAGE_H, M = 595, 842, 50

    def __init__(self, title, footer):
        self.title = _clean(title)
        self.footer = _clean(footer)
        self.pages = []
        self.cur = None
        self.y = 0
        self.new_page()

    # -- primitives --------------------------------------------------------
    def new_page(self):
        self.cur = []
        self.pages.append(self.cur)
        self.y = self.PAGE_H - self.M

    def width(self, s, size, bold=False):
        total = 0
        for ch in s:
            o = ord(ch)
            total += _W[o - 32] if 32 <= o <= 126 else 556
        return total * size / 1000.0 * (1.07 if bold else 1.0)

    def text(self, x, y, s, size=10, bold=False, color=DARK):
        r, g, b = color
        data = _esc(_clean(s))
        self.cur.append(f"BT /F{2 if bold else 1} {size} Tf {r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} Td ({data}) Tj ET")

    def rect(self, x, y, w, h, color):
        r, g, b = color
        self.cur.append(f"{r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")

    def wrap(self, s, size, maxw, bold=False):
        lines = []
        for raw in _clean(s).split("\n"):
            line = ""
            for word in raw.split():
                trial = (line + " " + word).strip()
                if self.width(trial, size, bold) <= maxw or not line:
                    line = trial
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        return lines

    def ensure(self, h):
        if self.y - h < self.M + 24:
            self.new_page()

    # -- blocks ------------------------------------------------------------
    def heading(self, s):
        self.ensure(60)
        self.y -= 18
        self.text(self.M, self.y, s, 14, True, PURPLE)
        self.y -= 7
        self.rect(self.M, self.y, 34, 2.2, PURPLE)
        self.y -= 16

    def para(self, s, size=10, indent=0, color=DARK, bold=False, gap=6, lead=1.5):
        maxw = self.PAGE_W - 2 * self.M - indent
        for line in self.wrap(s, size, maxw, bold):
            self.ensure(size * lead)
            self.text(self.M + indent, self.y, line, size, bold, color)
            self.y -= size * lead
        self.y -= gap

    def item(self, marker, s, size=10, indent=14, bold_prefix=None):
        maxw = self.PAGE_W - 2 * self.M - indent
        first = True
        full = (bold_prefix + " " if bold_prefix else "") + s
        for line in self.wrap(full, size, maxw):
            self.ensure(size * 1.5)
            if first:
                self.text(self.M, self.y, marker, size, True, PURPLE)
                first = False
            self.text(self.M + indent, self.y, line, size, False, DARK)
            self.y -= size * 1.5
        self.y -= 3

    # -- output ------------------------------------------------------------
    def build(self):
        n = len(self.pages)
        for i, ops in enumerate(self.pages):
            self.cur = ops
            self.rect(self.M, 36, self.PAGE_W - 2 * self.M, 0.6, (0.85, 0.85, 0.9))
            self.text(self.M, 24, self.footer, 8, False, GRAY)
            label = f"Page {i + 1} of {n}"
            self.text(self.PAGE_W - self.M - self.width(label, 8), 24, label, 8, False, GRAY)

        objs = [
            "<< /Type /Catalog /Pages 2 0 R >>",
            None,  # pages, filled below
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        ]
        kids = []
        for i, ops in enumerate(self.pages):
            page_id = 5 + 2 * i
            content_id = page_id + 1
            kids.append(f"{page_id} 0 R")
            objs.append(
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.PAGE_W} {self.PAGE_H}] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_id} 0 R >>"
            )
            stream = "\n".join(ops).encode("cp1252", "replace")
            objs.append(("stream", stream))
        objs[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {n} >>"
        stamp = datetime.datetime.now().strftime("D:%Y%m%d%H%M%S")
        objs.append(f"<< /Title ({_esc(self.title)}) /Producer (Xplorer Solution) /CreationDate ({stamp}) >>")
        info_id = len(objs)

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for i, o in enumerate(objs, start=1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode()
            if isinstance(o, tuple):
                out += f"<< /Length {len(o[1])} >>\nstream\n".encode() + o[1] + b"\nendstream"
            else:
                out += o.encode("cp1252", "replace")
            out += b"\nendobj\n"
        xref = len(out)
        out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R /Info {info_id} 0 R >>\n"
                f"startxref\n{xref}\n%%EOF\n").encode()
        return bytes(out)


def build_service_pdf(service, site):
    """Return the bytes of a brochure PDF for a Service model instance."""
    footer = " | ".join(x for x in [
        f"{site.site_name} {site.site_suffix}".strip(), site.email, site.phone] if x)
    pdf = _Pdf(f"{service.title} - Brochure", footer)

    # cover band
    band_h = 190
    pdf.rect(0, pdf.PAGE_H - band_h, pdf.PAGE_W, band_h, PURPLE)
    pdf.rect(0, pdf.PAGE_H - band_h, pdf.PAGE_W, 5, (0.30, 0.11, 0.58))
    y = pdf.PAGE_H - 62
    pdf.text(pdf.M, y, f"{site.site_name} {site.site_suffix}".upper().strip() + "  |  SERVICE BROCHURE", 9, True, SOFT)
    y -= 38
    for line in pdf.wrap(service.title, 26, pdf.PAGE_W - 2 * pdf.M, True):
        pdf.text(pdf.M, y, line, 26, True, WHITE)
        y -= 32
    tag = service.tagline or service.short_description
    for line in pdf.wrap(tag, 11.5, pdf.PAGE_W - 2 * pdf.M - 40)[:3]:
        pdf.text(pdf.M, y, line, 11.5, False, SOFT)
        y -= 16
    pdf.y = pdf.PAGE_H - band_h - 14

    pdf.heading("Overview")
    for p in service.guide_paragraphs:
        pdf.para(p)

    outcomes = list(service.outcomes.all())
    if outcomes:
        pdf.heading("Results you can expect")
        for o in outcomes:
            pdf.item("*", o.label, bold_prefix=o.value)

    ideal = service.ideal_for_list
    if ideal:
        pdf.heading("Who this is for")
        for x in ideal:
            pdf.item("-", x)

    feats = list(service.detail_features.all())
    if feats:
        pdf.heading("What's included")
        for f in feats:
            pdf.item("-", f.description, bold_prefix=f.title + ":")

    delivs = service.deliverable_list
    if delivs:
        pdf.heading("What you receive")
        for x in delivs:
            pdf.item("-", x)

    steps = list(service.detail_steps.all())
    if steps:
        pdf.heading("How we deliver")
        for i, st in enumerate(steps, 1):
            pdf.item(f"{i}.", st.description, indent=18, bold_prefix=st.title + ":")

    if service.tech_list:
        pdf.heading("Tools and technologies")
        pdf.para(", ".join(service.tech_list))

    faqs = list(service.detail_faqs.all())
    if faqs:
        pdf.heading("Frequently asked questions")
        for f in faqs:
            pdf.ensure(60)  # keep a question together with the start of its answer
            pdf.para(f.question, 10, 0, DARK, True, gap=1)
            pdf.para(f.answer, 10, 0, GRAY)

    pdf.heading("Let's talk")
    contact = [x for x in [site.email, site.phone, site.address] if x]
    pdf.para("Ready to start? Get in touch for a free consultation and a clear estimate.", gap=2)
    for c in contact:
        pdf.para(c, 10, 0, PURPLE, True, gap=0)
    return pdf.build()
