"""Make a CR80 portrait ID card (front + back) for each rep in ids.csv.

Usage:  python3 make_ids.py [ids.csv]
Needs:  pip install segno ; Node + Playwright ; pdfunite (poppler).

ids.csv columns:
  name, name_ur (optional), id_no (e.g. SVX-001), valid_until (e.g. 30 Nov 2027), photo (file in photos/, optional)
Office details (printed on the back) come from OFFICE below; edit them once.
Output: output/<id_no>.pdf (page 1 front, page 2 back), previews, ALL_id_cards.pdf
"""
import csv, html, re, subprocess, sys, urllib.parse
from pathlib import Path
import segno

# ---- Edit once: printed on the back of every card --------------------------
OFFICE = {
    "company": "[Solvexo contracting entity]",       # e.g. i9 Experts (Pvt) Ltd
    "phone": "[Office phone / WhatsApp]",             # as printed, e.g. 021-XXXXXXX
    "whatsapp": "923000000000",                       # 92 + 10 digits, used in the QR
    "address": "[Office address, Karachi]",
}
# ----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"; OUT.mkdir(exist_ok=True)
FONTS = (HERE.parent / "tent-card" / "fonts").as_uri()
template = (HERE / "template.html").read_text(encoding="utf-8")
SILHOUETTE = ('<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="120" fill="#EDE6E1"/>'
              '<circle cx="50" cy="46" r="20" fill="#C9B9AF"/><path d="M14 120c2-26 18-38 36-38s34 12 36 38z" fill="#C9B9AF"/>'
              '<text x="50" y="112" text-anchor="middle" font-family="Poppins" font-size="7" fill="#8E7F77">PHOTO</text></svg>')

def build(row):
    id_no = row["id_no"].strip().upper()
    if not re.fullmatch(r"[A-Z0-9-]{2,20}", id_no):
        raise ValueError(f"Bad id_no {id_no!r}")
    wa = re.sub(r"\D", "", OFFICE["whatsapp"])
    msg = f"Verify Solvexo rep ID {id_no}"
    qr = OUT / f"qr-{id_no}.svg"
    segno.make(f"https://wa.me/{wa}?text={urllib.parse.quote(msg)}", error="m").save(str(qr), scale=10, border=0, dark="#1F1A17", light=None)
    photo = (row.get("photo") or "").strip()
    photo_html = f'<img src="{(HERE / "photos" / photo).as_uri()}" alt="Photo of {html.escape(row["name"])}">' if photo else SILHOUETTE
    name_ur = (row.get("name_ur") or "").strip()
    page = (template
            .replace("{{NAME}}", html.escape(row["name"].strip()))
            .replace("{{NAME_UR_LINE}}", f'<p class="ur">{html.escape(name_ur)}</p>' if name_ur else "")
            .replace("{{ID_NO}}", id_no).replace("{{VALID}}", html.escape(row["valid_until"].strip()))
            .replace("{{PHOTO}}", photo_html).replace("{{QR_FILE}}", qr.as_uri())
            .replace("{{OFFICE_PHONE}}", html.escape(OFFICE["phone"]))
            .replace("{{COMPANY}}", html.escape(OFFICE["company"]))
            .replace("{{OFFICE_ADDRESS}}", html.escape(OFFICE["address"]))
            .replace("url(FONTS/", f"url({FONTS}/")
            .replace('src="LOGO"', f'src="{(HERE / "logo.png").as_uri()}"'))
    src = OUT / f"{id_no}.html"; src.write_text(page, encoding="utf-8")
    pdf = OUT / f"{id_no}.pdf"
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(pdf), str(OUT / id_no)], check=True)
    return pdf

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ids.csv"
    pdfs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pdfs.append(build(row)); print("made", pdfs[-1].name)
    if len(pdfs) > 1:
        subprocess.run(["pdfunite", *map(str, pdfs), str(OUT / "ALL_id_cards.pdf")], check=True)
