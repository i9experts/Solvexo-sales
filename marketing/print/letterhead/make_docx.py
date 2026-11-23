"""Build the editable Word letterhead template: output/Solvexo_Letterhead_Template.docx"""
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = RGBColor(0xD9, 0x77, 0x57); R = RGBColor(0xB8, 0x5C, 0x3E); INK = RGBColor(0x1F, 0x1A, 0x17); MUTE = RGBColor(0x5E, 0x53, 0x4D)

def run(p, text, size=9, bold=False, color=INK):
    r = p.add_run(text); r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = "Arial"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial"); return r

def border_bottom(p, color="D97757", sz=10):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "6"), ("w:color", color)): e.set(qn(k), v)
    b.append(e); pPr.append(b)

def border_top(p, color="EAD9CF", sz=4):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:top")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "4"), ("w:color", color)): e.set(qn(k), v)
    b.append(e); pPr.append(b)

def no_borders(tbl):
    tblPr = tbl._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "nil"); b.append(e)
    tblPr.append(b)

def page_field(p):
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        r = p.add_run(); r.font.size = Pt(7); r.font.color.rgb = MUTE
        if kind:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), kind); r._r.append(f)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._r.append(it)

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10.5); st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.25

s = doc.sections[0]
s.page_width, s.page_height = Mm(210), Mm(297)
s.left_margin = s.right_margin = Mm(25); s.top_margin = Mm(48); s.bottom_margin = Mm(30)
s.header_distance = Mm(14); s.footer_distance = Mm(12)
s.different_first_page_header_footer = True

# ---- first-page header: logo | contact, then rule
h = s.first_page_header
tbl = h.add_table(rows=1, cols=2, width=Mm(160)); no_borders(tbl); tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
c0, c1 = tbl.rows[0].cells
c0.width = Mm(70); c1.width = Mm(90)
c0.paragraphs[0].add_run().add_picture(str(HERE / "logo.png"), height=Mm(12))
p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run(p, "[Company legal name]\n", 8, True)
run(p, "[Street address], [Area], Karachi, Pakistan\n", 7.5, color=MUTE)
run(p, "[+92 XX XXXX XXXX] · ", 7.5, color=MUTE); run(p, "sales@solvexo.store\n", 7.5, True, R)
run(p, "solvexo.store", 7.5, True, R)
hp = h.paragraphs[0]; hp.paragraph_format.space_after = Pt(0)
rule = h.add_paragraph(); border_bottom(rule, "D97757", 10); rule.paragraph_format.space_after = Pt(0)

# ---- continuation header
h2 = s.header; p = h2.paragraphs[0]
p.add_run().add_picture(str(HERE / "icon.png"), height=Mm(8))
run(p, "\tSOLVEXO · CONTINUED", 7, color=MUTE)
p.paragraph_format.tab_stops.add_tab_stop(Mm(159), alignment=WD_TAB_ALIGNMENT.RIGHT)
border_bottom(p, "EAD9CF", 4)

# ---- footers (first + continuation): 2-column borderless table
for f, left in ((s.first_page_footer, "Solvexo · Create. Sell. Manage. Grow. · Powered by i9 Experts"),
                (s.footer, "Solvexo · solvexo.store · sales@solvexo.store")):
    top = f.paragraphs[0]; border_top(top); top.paragraph_format.space_after = Pt(0)
    ft = f.add_table(rows=1, cols=2, width=Mm(160)); no_borders(ft)
    a, b = ft.rows[0].cells; a.width = Mm(110); b.width = Mm(50)
    run(a.paragraphs[0], left, 7, color=MUTE)
    pb = b.paragraphs[0]; pb.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(pb, "NTN [_______] · Page ", 7, color=MUTE); page_field(pb)

# ---- sample letter body (replace the bracketed text)
def para(text, size=10.5, bold=False, color=INK, after=6):
    p = doc.add_paragraph(); run(p, text, size, bold, color); p.paragraph_format.space_after = Pt(after); return p
para("[Date, e.g. 24 November 2026]", after=2)
para("Ref: SVX/[YYYY]/[___]", 9, color=MUTE, after=14)
para("[Recipient name]", bold=True, after=0); para("[Designation]", after=0); para("[Company]", after=0); para("[Address]", after=14)
p = doc.add_paragraph(); run(p, "Subject: ", 10.5, True); run(p, "[Subject of the letter]", 10.5, True); p.paragraph_format.space_after = Pt(12)
para("Dear [Name],", after=10)
para("[Opening paragraph: the purpose of the letter.]")
para("[Body: details, terms or next steps. Keep paragraphs short. Use only approved claims and current published prices.]")
para("[Closing paragraph: what you would like the reader to do, and by when.]", after=16)
para("Sincerely,", after=30)
para("[Name]", bold=True, after=0); para("[Designation]", after=0); para("[Company legal name] · Solvexo", color=MUTE, after=0)

out = HERE / "output" / "Solvexo_Letterhead_Template.docx"; doc.save(out); print("saved", out.name)
