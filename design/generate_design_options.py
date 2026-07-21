#!/usr/bin/env python3
"""Generate design-options.pdf: colour schemes + layout options for the
S&S Property Services website.

Every colour scheme is shown as a real rendered preview of the site with
that scheme applied, plus its five hex codes in the same order as the CSS
variables at the top of index.html (--primary, --dark, --accent, --light,
--ink), so a scheme can be applied by copying its five values straight
into the stylesheet.

Usage:
    node render_scheme_previews.js <previews-dir>   # render previews first
    python3 generate_design_options.py <previews-dir>
"""
import json
import os
import sys

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

W, H = letter
M = 54  # page margin

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "schemes.json")) as f:
    SCHEMES = [tuple(s) for s in json.load(f)]

LAYOUTS = [
    ("Layout A — Classic Stack (current build)",
     "Full-width hero with headline left and checklist card right, service cards in a row, "
     "photo grid, testimonials, then quote + inquiry forms side by side on a dark band."),
    ("Layout B — Split Photo Hero",
     "Hero split 50/50: text and buttons on the left, a large photo on the right. "
     "Feels personal — great once you have a photo of the two of you with your gear."),
    ("Layout C — Full-Bleed Photo Hero",
     "One big background photo behind the headline with a dark overlay. Dramatic first "
     "impression; works best with a strong wide lawn/house shot."),
    ("Layout D — Sticky Quote Sidebar",
     "Content scrolls on the left while a compact quote form stays pinned on the right. "
     "Maximizes quote requests; form is always one glance away."),
    ("Layout E — Zig-Zag Services",
     "Each service gets its own row, alternating photo-left/text-right then text-left/photo-right. "
     "More room to sell each service; page gets longer."),
    ("Layout F — Photo Mosaic First",
     "Leads with a big mosaic gallery under a slim header — the work speaks first. "
     "Best once you've replaced stock photos with real before/afters."),
    ("Layout G — One-Page Minimal",
     "Single narrow column, generous whitespace, oversized type, small underline accents. "
     "Modern and fast; suits the Graphite Mono or Sage & Stone schemes."),
    ("Layout H — Boxed & Framed",
     "All content sits in a centred card 'frame' floating over a tinted background. "
     "Tidy, brochure-like feel; pairs well with warm schemes."),
    ("Layout I — Services-First Landing",
     "Slim banner up top, then straight into big clickable service tiles that jump to "
     "detail sections. Good for visitors who already know what they need."),
    ("Layout J — Testimonial Spotlight",
     "A full-width rotating testimonial band sits mid-page between services and gallery, "
     "with star ratings front and centre. Leans on social proof to win trust."),
]

GREY = HexColor("#e8e8e8")
MIDGREY = HexColor("#c9c9c9")
DARKTXT = HexColor("#222222")
SUBTXT = HexColor("#666666")
BRAND = HexColor("#2e7d32")
BRANDDARK = HexColor("#1b3022")
ACCENT = HexColor("#f9a825")

SCHEME_PAGES = (len(SCHEMES) + 1) // 2  # 2 schemes per page
FIRST_SCHEME_PAGE = 3
FIRST_LAYOUT_PAGE = FIRST_SCHEME_PAGE + SCHEME_PAGES


def footer(c, page_no):
    c.setFont("Helvetica", 8)
    c.setFillColor(SUBTXT)
    c.drawString(M, 30, "S&S Property Services - Website Design Options")
    c.drawRightString(W - M, 30, str(page_no))


def cover(c):
    c.setFillColor(BRANDDARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BRAND)
    c.rect(0, H - 260, W, 8, fill=1, stroke=0)
    for i, s in enumerate(SCHEMES[:12]):
        c.setFillColor(HexColor(s[2]))
        c.rect(M + i * ((W - 2 * M) / 12), 120, (W - 2 * M) / 12 - 4, 26, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 34)
    c.drawString(M, H - 200, "S&S Property Services")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawString(M, H - 232, "Website Design Options")
    c.setFillColor(HexColor("#cfdad2"))
    c.setFont("Helvetica", 12)
    c.drawString(M, H - 280, f"{len(SCHEMES)} colour schemes  +  {len(LAYOUTS)} page layouts  =  "
                             f"{len(SCHEMES) + len(LAYOUTS)} options to mix and match")
    c.setFont("Helvetica", 10)
    c.drawString(M, H - 300, "Every colour scheme is shown applied to the real website.")
    c.drawString(M, H - 316, "Pick one colour scheme and one layout - any combination works.")
    c.drawString(M, 90, "Prepared July 2026")
    c.showPage()


def howto(c):
    c.setFillColor(DARKTXT)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - 80, "How to use this document")
    c.setFont("Helvetica", 11)
    c.setFillColor(SUBTXT)
    y = H - 115
    last = FIRST_SCHEME_PAGE + SCHEME_PAGES - 1
    for line in [
        f"1.  Flip through the colour schemes (pages {FIRST_SCHEME_PAGE}-{last}). Each one shows",
        "     the actual website rendered in that scheme, plus its five colours with hex codes:",
        "     PRIMARY (buttons & links), DARK (headings & footer), ACCENT (highlights),",
        "     LIGHT (section backgrounds) and INK (body text).",
        "",
        "2.  The website is built so any scheme can be applied in under a minute: open index.html",
        "     and replace the five hex values at the top of the stylesheet (they're labelled the",
        "     same way) with the five codes from your chosen scheme.",
        "",
        f"3.  Then browse the layouts (pages {FIRST_LAYOUT_PAGE}-{FIRST_LAYOUT_PAGE + 4}). Each is shown as a wireframe example.",
        "     Layout A is what's built now; the others re-arrange the same sections, so",
        "     switching later is straightforward.",
        "",
        "4.  Shortlist 2-3 combinations you both like, and we'll mock them up.",
    ]:
        c.drawString(M, y, line)
        y -= 16
    box_y = y - 150
    c.setFillColor(HexColor("#f4f4f4"))
    c.roundRect(M, box_y, W - 2 * M, 140, 8, fill=1, stroke=0)
    c.setFont("Courier-Bold", 10)
    c.setFillColor(DARKTXT)
    c.drawString(M + 16, box_y + 116, "Example - applying scheme 1 'Fresh Fairway' in index.html:")
    c.setFont("Courier", 10)
    for i, line in enumerate([
        ":root{",
        "  --primary: #2e7d32;   /* buttons, links, accents  */",
        "  --dark:    #1b3022;   /* headings, footer         */",
        "  --accent:  #f9a825;   /* call-to-action highlights */",
        "  --light:   #f4f7f2;   /* section backgrounds      */",
        "  --ink:     #26302b;   /* body text                */",
        "}",
    ]):
        c.drawString(M + 16, box_y + 96 - i * 13, line)
    footer(c, 2)
    c.showPage()


def preview_jpeg(previews_dir, idx):
    """Load scheme preview PNG, downscale, return as ImageReader + aspect."""
    src = os.path.join(previews_dir, f"scheme-{idx:02d}.png")
    jpg = os.path.join(previews_dir, f"scheme-{idx:02d}.jpg")
    if not os.path.exists(jpg):
        im = Image.open(src).convert("RGB")
        im.thumbnail((820, 820), Image.LANCZOS)
        im.save(jpg, "JPEG", quality=80)
    im = Image.open(jpg)
    return ImageReader(jpg), im.size[1] / im.size[0]


def scheme_block(c, previews_dir, top, block_h, idx, s):
    """One scheme: info + swatches on the left, live preview on the right."""
    name, vibe, *cols = s
    labels = ["PRIMARY", "DARK", "ACCENT", "LIGHT", "INK"]
    left_w = 168
    img_w = W - 2 * M - left_w - 16
    img, aspect = preview_jpeg(previews_dir, idx)
    img_h = min(block_h - 30, img_w * aspect)

    c.setFillColor(DARKTXT)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(M, top - 16, f"{idx}.  {name}")
    c.setFillColor(SUBTXT)
    wrap_text(c, vibe, M, top - 32, left_w, size=8.5, leading=11)

    # vertical swatch list
    sw_h = 22
    sy = top - 66
    for label, col in zip(labels, cols):
        c.setFillColor(HexColor(col))
        c.setStrokeColor(MIDGREY)
        c.roundRect(M, sy - sw_h, 46, sw_h - 4, 3, fill=1, stroke=1)
        c.setFillColor(DARKTXT)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(M + 54, sy - 11, label)
        c.setFont("Courier", 8)
        c.drawString(M + 54, sy - 20, col)
        sy -= sw_h

    # preview screenshot
    ix = M + left_w + 16
    iy = top - 16 - img_h
    c.drawImage(img, ix, iy, width=img_w, height=img_h)
    c.setStrokeColor(MIDGREY)
    c.rect(ix, iy, img_w, img_h, fill=0, stroke=1)


def schemes_pages(c, previews_dir):
    per_page = 2
    block_h = (H - 130) / per_page
    page = FIRST_SCHEME_PAGE
    for p in range(0, len(SCHEMES), per_page):
        c.setFillColor(DARKTXT)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(M, H - 60, "Colour Schemes - applied to the site")
        c.setFont("Helvetica", 10)
        c.setFillColor(SUBTXT)
        c.drawRightString(W - M, H - 60, f"schemes {p + 1}-{min(p + per_page, len(SCHEMES))} of {len(SCHEMES)}")
        for i, s in enumerate(SCHEMES[p:p + per_page]):
            top = H - 80 - i * block_h
            scheme_block(c, previews_dir, top, block_h - 12, p + i + 1, s)
        footer(c, page)
        c.showPage()
        page += 1


# ---- wireframe drawing helpers ----
def block(c, x, y, w, h, col=GREY, r=3):
    c.setFillColor(col)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)


def lines(c, x, y, w, n, gap=5):
    c.setFillColor(MIDGREY)
    for i in range(n):
        c.rect(x, y - i * gap, w * (0.95 if i % 2 == 0 else 0.7), 2.4, fill=1, stroke=0)


def frame(c, x, y, w, h):
    c.setFillColor(HexColor("#ffffff"))
    c.setStrokeColor(MIDGREY)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    block(c, x + 6, y + h - 16, w - 12, 10, GREY)
    block(c, x + 10, y + h - 14, 22, 6, BRAND)
    block(c, x + w - 34, y + h - 14, 24, 6, ACCENT, r=3)


def wf_classic(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 66, w - 12, 46, BRANDDARK)
    lines(c, x + 14, y + h - 32, w * 0.35, 3, 7)
    block(c, x + w * 0.55, y + h - 60, w * 0.38, 34, HexColor("#3a5545"))
    cw = (w - 12 - 18) / 4
    for i in range(4):
        block(c, x + 6 + i * (cw + 6), y + h - 96, cw, 24)
    for i in range(3):
        block(c, x + 6 + i * ((w - 24) / 3 + 6), y + h - 128, (w - 24) / 3, 26, MIDGREY)
    block(c, x + 6, y + 8, w - 12, h - 144, BRANDDARK)
    block(c, x + 12, y + 12, (w - 24) * 0.55, h - 152, HexColor("#ffffff"))
    block(c, x + 16 + (w - 24) * 0.55, y + 12, (w - 24) * 0.4, h - 152, HexColor("#ffffff"))


def wf_split(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 76, (w - 12) / 2 - 3, 56, HexColor("#f0f0f0"))
    lines(c, x + 14, y + h - 34, w * 0.3, 4, 8)
    block(c, x + 14, y + h - 70, 30, 8, BRAND)
    block(c, x + 6 + (w - 12) / 2 + 3, y + h - 76, (w - 12) / 2 - 3, 56, MIDGREY)
    for i in range(4):
        cw = (w - 12 - 18) / 4
        block(c, x + 6 + i * (cw + 6), y + h - 106, cw, 22)
    block(c, x + 6, y + 8, w - 12, h - 122, GREY)


def wf_fullbleed(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 90, w - 12, 70, HexColor("#5a6a5e"))
    c.setFillColor(HexColor("#ffffff"))
    c.rect(x + w * 0.28, y + h - 50, w * 0.44, 4, fill=1, stroke=0)
    c.rect(x + w * 0.34, y + h - 60, w * 0.32, 3, fill=1, stroke=0)
    block(c, x + w * 0.42, y + h - 80, w * 0.16, 9, ACCENT)
    for i in range(4):
        cw = (w - 12 - 18) / 4
        block(c, x + 6 + i * (cw + 6), y + h - 120, cw, 22)
    block(c, x + 6, y + 8, w - 12, h - 136, GREY)


def wf_sidebar(c, x, y, w, h):
    frame(c, x, y, w, h)
    main_w = (w - 12) * 0.62
    block(c, x + 6, y + h - 60, main_w, 40, BRANDDARK)
    block(c, x + 6, y + h - 92, main_w, 26, GREY)
    block(c, x + 6, y + h - 124, main_w, 26, MIDGREY)
    block(c, x + 6, y + 8, main_w, h - 140, GREY)
    fx = x + 10 + main_w
    block(c, fx, y + 8, w - 16 - main_w, h - 28, HexColor("#ffffff"))
    c.setStrokeColor(BRAND)
    c.roundRect(fx, y + 8, w - 16 - main_w, h - 28, 3, fill=0, stroke=1)
    for i in range(5):
        block(c, fx + 5, y + h - 40 - i * 14, w - 26 - main_w, 8, GREY)
    block(c, fx + 5, y + 14, w - 26 - main_w, 10, BRAND)


def wf_zigzag(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 44, w - 12, 24, BRANDDARK)
    rows = 4
    rh = (h - 60) / rows - 6
    for i in range(rows):
        ry = y + 8 + (rows - 1 - i) * (rh + 6)
        if i % 2 == 0:
            block(c, x + 6, ry, (w - 12) * 0.45, rh, MIDGREY)
            lines(c, x + 12 + (w - 12) * 0.45, ry + rh - 8, w * 0.4, 3, 7)
        else:
            lines(c, x + 12, ry + rh - 8, w * 0.4, 3, 7)
            block(c, x + 6 + (w - 12) * 0.55, ry, (w - 12) * 0.45, rh, MIDGREY)


def wf_mosaic(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 36, w - 12, 16, GREY)
    gx, gy = x + 6, y + h - 42
    block(c, gx, gy - 52, (w - 16) * 0.5, 52, MIDGREY)
    block(c, gx + (w - 16) * 0.5 + 4, gy - 24, (w - 16) * 0.5, 24, HexColor("#b5c4b5"))
    block(c, gx + (w - 16) * 0.5 + 4, gy - 52, (w - 16) * 0.5, 24, GREY)
    block(c, gx, gy - 80, (w - 16) * 0.33, 24, GREY)
    block(c, gx + (w - 16) * 0.33 + 4, gy - 80, (w - 16) * 0.33, 24, HexColor("#b5c4b5"))
    block(c, gx + (w - 16) * 0.66 + 8, gy - 80, (w - 16) * 0.33, 24, MIDGREY)
    block(c, x + 6, y + 8, w - 12, h - 132, BRANDDARK)


def wf_minimal(c, x, y, w, h):
    frame(c, x, y, w, h)
    cx = x + w * 0.2
    cw = w * 0.6
    c.setFillColor(DARKTXT)
    c.rect(cx, y + h - 40, cw * 0.8, 5, fill=1, stroke=0)
    c.rect(cx, y + h - 50, cw * 0.5, 4, fill=1, stroke=0)
    block(c, cx, y + h - 58, 26, 4, BRAND)
    lines(c, cx, y + h - 72, cw, 4, 7)
    block(c, cx, y + h - 118, cw, 12, GREY)
    lines(c, cx, y + h - 140, cw, 3, 7)
    block(c, cx, y + 14, cw * 0.35, 10, BRANDDARK)


def wf_boxed(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + 8, w - 12, h - 28, HexColor("#dfe8df"))
    bx, bw = x + w * 0.12, w * 0.76
    block(c, bx, y + 16, bw, h - 44, HexColor("#ffffff"), r=5)
    block(c, bx + 8, y + h - 64, bw - 16, 28, BRANDDARK)
    for i in range(3):
        cw2 = (bw - 16 - 12) / 3
        block(c, bx + 8 + i * (cw2 + 6), y + h - 96, cw2, 22, GREY)
    block(c, bx + 8, y + 24, bw - 16, h - 128, GREY)


def wf_servicesfirst(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 38, w - 12, 18, BRANDDARK)
    cw = (w - 12 - 6) / 2
    for i in range(2):
        for j in range(2):
            block(c, x + 6 + j * (cw + 6), y + h - 44 - (i + 1) * 34, cw, 28,
                  HexColor("#cfe0cf") if (i + j) % 2 == 0 else GREY)
    block(c, x + 6, y + 8, w - 12, h - 124, MIDGREY)


def wf_spotlight(c, x, y, w, h):
    frame(c, x, y, w, h)
    block(c, x + 6, y + h - 52, w - 12, 32, BRANDDARK)
    for i in range(4):
        cw = (w - 12 - 18) / 4
        block(c, x + 6 + i * (cw + 6), y + h - 82, cw, 22)
    band_y = y + h - 122
    block(c, x + 6, band_y, w - 12, 32, ACCENT)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, band_y + 19, '* * * * *')
    c.rect(x + w * 0.25, band_y + 8, w * 0.5, 3, fill=1, stroke=0)
    block(c, x + 6, y + 8, w - 12, band_y - y - 14, GREY)


WIREFRAMES = [wf_classic, wf_split, wf_fullbleed, wf_sidebar, wf_zigzag,
              wf_mosaic, wf_minimal, wf_boxed, wf_servicesfirst, wf_spotlight]


def wrap_text(c, text, x, y, max_w, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    words, line = text.split(), ""
    for word in words:
        trial = (line + " " + word).strip()
        if c.stringWidth(trial, font, size) > max_w:
            c.drawString(x, y, line)
            y -= leading
            line = word
        else:
            line = trial
    if line:
        c.drawString(x, y, line)
    return y


def layout_pages(c):
    page = FIRST_LAYOUT_PAGE
    per_page = 2
    for p in range(0, len(LAYOUTS), per_page):
        c.setFillColor(DARKTXT)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(M, H - 60, "Page Layouts - wireframe examples")
        c.setFont("Helvetica", 10)
        c.setFillColor(SUBTXT)
        c.drawRightString(W - M, H - 60, f"layouts {p + 1}-{min(p + per_page, len(LAYOUTS))} of {len(LAYOUTS)}")
        for i, (title, desc) in enumerate(LAYOUTS[p:p + per_page]):
            top = H - 90 - i * ((H - 140) / per_page)
            wf_w, wf_h = 210, 260
            WIREFRAMES[p + i](c, M, top - wf_h, wf_w, wf_h)
            tx = M + wf_w + 24
            c.setFillColor(DARKTXT)
            c.setFont("Helvetica-Bold", 12.5)
            c.drawString(tx, top - 24, title)
            c.setFillColor(SUBTXT)
            wrap_text(c, desc, tx, top - 44, W - M - tx)
        footer(c, page)
        c.showPage()
        page += 1


def main():
    previews_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "previews")
    missing = [i for i in range(1, len(SCHEMES) + 1)
               if not os.path.exists(os.path.join(previews_dir, f"scheme-{i:02d}.png"))
               and not os.path.exists(os.path.join(previews_dir, f"scheme-{i:02d}.jpg"))]
    if missing:
        sys.exit(f"Missing previews {missing} in {previews_dir} - "
                 f"run: node render_scheme_previews.js {previews_dir}")
    out = os.path.join(HERE, "..", "design-options.pdf")
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle("S&S Property Services - Website Design Options")
    cover(c)
    howto(c)
    schemes_pages(c, previews_dir)
    layout_pages(c)
    c.save()
    print(f"Wrote {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
