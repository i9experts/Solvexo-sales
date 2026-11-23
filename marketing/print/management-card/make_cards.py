"""Make a management business card for each person in managers.csv.

Usage:  python3 make_cards.py [managers.csv]
Needs:  pip install segno pypdf ; Node + Playwright.
CSV columns: name, title, phone (as printed), email, whatsapp (optional, 92 + 10 digits), linkedin (optional, e.g. linkedin.com/in/name)
Output per person (output/):
  <slug>_print.pdf     page 1 front, page 2 back
  <slug>_spotuv.pdf    page 1 front mask (logo), page 2 back mask (icon): black = gloss varnish
  <slug>_front.png / _back.png previews
The QR on the back is a vCard: scanning it offers to save the person as a phone contact.
"""
import csv, html, re, subprocess, sys
from pathlib import Path
import segno
import segno.helpers
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"; OUT.mkdir(exist_ok=True)
FONTS = (HERE.parent / "tent-card" / "fonts").as_uri()
template = (HERE / "template.html").read_text(encoding="utf-8")
ORG = "Solvexo"

def build(row):
    name = row["name"].strip(); slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    parts = name.split(); last = parts[-1] if len(parts) > 1 else ""; first = " ".join(parts[:-1]) if last else name
    phone = row["phone"].strip(); email = row["email"].strip(); title = row["title"].strip()
    linkedin = (row.get("linkedin") or "").strip()
    qr = OUT / f"qr-{slug}.svg"
    segno.helpers.make_vcard(name=f"{last};{first}", displayname=name, org=ORG, title=title,
                             phone=phone, email=email, url="https://solvexo.store").save(
        str(qr), scale=10, border=0, dark="#1F1A17", light=None)
    li = ('<div class="ln"><i><svg width="8" height="8" viewBox="0 0 24 24" fill="#F59373"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.1c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4z"/></svg></i>'
          f'<span>{html.escape(linkedin)}</span></div>') if linkedin else ""
    page = (template.replace("{{NAME}}", html.escape(name)).replace("{{TITLE}}", html.escape(title.upper()))
            .replace("{{PHONE}}", html.escape(phone)).replace("{{EMAIL}}", html.escape(email))
            .replace("{{LINKEDIN_LINE}}", li).replace("{{QR_FILE}}", qr.as_uri())
            .replace("url(FONTS/", f"url({FONTS}/")
            .replace('src="LOGO_LIGHT"', f'src="{(HERE / "logo-light.png").as_uri()}"')
            .replace('src="ICON"', f'src="{(HERE / "icon.png").as_uri()}"'))
    src = OUT / f"{slug}.html"; src.write_text(page, encoding="utf-8")
    allpdf = OUT / f"{slug}_all.pdf"
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(allpdf), str(OUT / slug)], check=True)
    r = PdfReader(str(allpdf))
    for name_, idx in (("print", [0, 1]), ("spotuv", [3, 2])):
        w = PdfWriter()
        for i in idx: w.add_page(r.pages[i])
        w.write(str(OUT / f"{slug}_{name_}.pdf"))
    allpdf.unlink()
    return slug

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "managers.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            print("made", build(row))
