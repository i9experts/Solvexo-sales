"""Make a personalised visiting card (front + back) for each rep in reps.csv.

Usage:  python3 make_cards.py [reps.csv]
Needs:  pip install segno ; Node + Playwright ; pdfunite (poppler).
CSV columns:
  name      - as printed, e.g. "Ahmed Raza"
  name_ur   - optional Urdu name, e.g. "احمد رضا"
  title     - e.g. "Seller Success" (printed in capitals)
  phone     - as printed, e.g. "0300-1234567"
  whatsapp  - international digits for the QR, e.g. "923001234567"
  email     - optional
Output: output/<slug>.pdf (page 1 front, page 2 back), output/<slug>_front.png / _back.png, output/ALL_rep_cards.pdf
"""
import csv, html, re, subprocess, sys, urllib.parse
from pathlib import Path
import segno

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
FONTS = (HERE.parent / "tent-card" / "fonts").as_uri()
template = (HERE / "template.html").read_text(encoding="utf-8")
GREETING = "Salam, I'd like a Solvexo demo for my shop."

def build(row):
    name = row["name"].strip()
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "rep"
    wa = re.sub(r"\D", "", row["whatsapp"])
    if not re.fullmatch(r"92\d{10}", wa):
        raise ValueError(f"{name}: whatsapp must be 92 + 10 digits, got {row['whatsapp']!r}")
    qr = OUT / f"qr-{slug}.svg"
    segno.make(f"https://wa.me/{wa}?text={urllib.parse.quote(GREETING)}", error="m").save(
        str(qr), scale=10, border=0, dark="#1F1A17", light=None)
    name_ur = (row.get("name_ur") or "").strip()
    email = (row.get("email") or "").strip()
    page = (template
            .replace("{{NAME}}", html.escape(name))
            .replace("{{NAME_UR_LINE}}", f'<p class="ur">{html.escape(name_ur)}</p>' if name_ur else "")
            .replace("{{TITLE}}", html.escape(row["title"].strip().upper()))
            .replace("{{PHONE}}", html.escape(row["phone"].strip()))
            .replace("{{EMAIL_LINE}}", (
                '<div class="ln"><i><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#B85C3E" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></i>'
                f'<span>{html.escape(email)}</span></div>') if email else "")
            .replace("{{QR_FILE}}", qr.as_uri())
            .replace("url(FONTS/", f"url({FONTS}/")
            .replace('class="logo" src="LOGO"', f'class="logo" src="{(HERE / "logo.png").as_uri()}"'))
    src = OUT / f"{slug}.html"
    src.write_text(page, encoding="utf-8")
    pdf = OUT / f"{slug}.pdf"
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(pdf), str(OUT / slug)], check=True)
    return pdf

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "reps.csv"
    pdfs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pdfs.append(build(row)); print("made", pdfs[-1].name)
    if len(pdfs) > 1:
        subprocess.run(["pdfunite", *map(str, pdfs), str(OUT / "ALL_rep_cards.pdf")], check=True)
