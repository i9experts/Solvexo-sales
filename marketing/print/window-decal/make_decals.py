"""Make a personalised 6 x 6 in window/door decal for each seller.

Usage:  python3 make_decals.py [sellers.csv]
        (defaults to ../tent-card/sellers.csv, so one seller list makes both items)
Needs:  pip install segno ; Node + Playwright ; pdfunite (poppler).
Output, per seller in output/:
  <sub>_outside.pdf  for opaque white vinyl stuck on the OUTSIDE of the glass (reads normally)
  <sub>_inside.pdf   mirrored, for clear vinyl stuck on the INSIDE of the glass, read through it
  <sub>.png          preview
  ALL_decals_outside.pdf, ALL_decals_inside.pdf
"""
import csv, html, re, subprocess, sys
from pathlib import Path
import segno
from pypdf import PdfReader, PdfWriter, Transformation

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
FONTS = (HERE.parent / "tent-card" / "fonts").as_uri()
ICON = (HERE / "icon.png").as_uri()
template = (HERE / "template.html").read_text(encoding="utf-8")

def build(store_name, subdomain):
    sub = subdomain.strip().lower()
    if not re.fullmatch(r"[a-z0-9-]{1,63}", sub):
        raise ValueError(f"Bad subdomain: {subdomain!r}")
    url = f"https://{sub}.solvexo.store/?utm_source=windowdecal&utm_medium=print"
    qr = OUT / f"qr-{sub}.svg"
    segno.make(url, error="q").save(str(qr), scale=10, border=0, dark="#1F1A17", light=None)
    page = (template
            .replace("{{STORE_NAME}}", html.escape(store_name.strip()))
            .replace("{{STORE_URL_TEXT}}", f"{sub}.solvexo.store")
            .replace("{{QR_FILE}}", qr.as_uri())
            .replace("url(FONTS/", f"url({FONTS}/").replace('src="ICON"', f'src="{ICON}"'))
    src = OUT / f"{sub}.html"
    src.write_text(page, encoding="utf-8")
    outside, inside = OUT / f"{sub}_outside.pdf", OUT / f"{sub}_inside.pdf"
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(outside), str(OUT / f"{sub}.png")], check=True)
    # Mirror the finished page (keeps Urdu shaping intact) for inside-the-glass clear vinyl
    r = PdfReader(str(outside)); w = PdfWriter()
    pg = r.pages[0]; width = float(pg.mediabox.width)
    pg.add_transformation(Transformation().scale(-1, 1).translate(width, 0))
    w.add_page(pg); w.write(str(inside))
    made = {"outside": outside, "inside": inside}
    return made

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "tent-card" / "sellers.csv"
    allm = {"outside": [], "inside": []}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m = build(row["store_name"], row["subdomain"])
            for k in allm: allm[k].append(m[k])
            print("made", row["subdomain"])
    for k, files in allm.items():
        if len(files) > 1:
            subprocess.run(["pdfunite", *map(str, files), str(OUT / f"ALL_decals_{k}.pdf")], check=True)
