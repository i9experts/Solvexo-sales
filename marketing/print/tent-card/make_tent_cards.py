"""Make a personalised counter tent card for each seller in sellers.csv.

Usage:  python3 make_tent_cards.py [sellers.csv]
Needs:  pip install segno ; Node + Playwright (for render.js) ; pdfunite (poppler) for the combined file.
Output: output/<subdomain>.pdf (print), output/<subdomain>.png (preview), output/ALL_tent_cards.pdf
"""
import csv, html, re, subprocess, sys
from pathlib import Path
import segno

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
template = (HERE / "template.html").read_text(encoding="utf-8")
m = re.search(r"<!--PANEL-->(.*?)<!--/PANEL-->", template, re.S)
panel = m.group(1)

def build(store_name, subdomain):
    sub = subdomain.strip().lower()
    if not re.fullmatch(r"[a-z0-9-]{1,63}", sub):
        raise ValueError(f"Bad subdomain: {subdomain!r}")
    url = f"https://{sub}.solvexo.store/?utm_source=tentcard&utm_medium=print"
    qr_name = f"qr-{sub}.svg"
    segno.make(url, error="m").save(str(OUT / qr_name), scale=10, border=0, dark="#1F1A17", light=None)
    fill = lambda pos: (panel.replace("{{POS}}", pos)
                        .replace("{{STORE_NAME}}", html.escape(store_name.strip()))
                        .replace("{{STORE_URL_TEXT}}", f"{sub}.solvexo.store")
                        .replace("{{QR_FILE}}", qr_name))
    page = template.replace(m.group(0), fill("top") + fill("bot"))
    # assets live one folder up from output/
    page = page.replace("url(fonts/", "url(../fonts/").replace('src="icon.png"', 'src="../icon.png"')
    src = OUT / f"{sub}.html"
    src.write_text(page, encoding="utf-8")
    pdf, png = OUT / f"{sub}.pdf", OUT / f"{sub}.png"
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(pdf), str(png)], check=True)
    return pdf

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sellers.csv"
    pdfs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pdfs.append(build(row["store_name"], row["subdomain"]))
            print("made", pdfs[-1].name)
    if len(pdfs) > 1:
        subprocess.run(["pdfunite", *map(str, pdfs), str(OUT / "ALL_tent_cards.pdf")], check=True)
        print("made ALL_tent_cards.pdf")
