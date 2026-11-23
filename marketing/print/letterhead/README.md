# Letterhead (F1): A4

Two versions from one design:

1. **Print letterhead** (`output/letterhead_print.pdf`): page 1 is the first sheet (logo, contact block, black-and-terracotta rule, coral corner, footer with NTN/registered office, terracotta band at the foot); page 2 is the continuation sheet (icon, "SOLVEXO · CONTINUED", footer). A4 + 3 mm bleed; 100 gsm uncoated bond (prints well on office laser printers afterwards). 500 sheets page 1 + 250 continuation.
2. **Word template** (`output/Solvexo_Letterhead_Template.docx`): the same header and footer built into Word (first-page header + continuation header, page numbers), with a sample letter (date, ref no., recipient, subject, body, signature block) to overwrite. Body font Arial (installed everywhere).

**Writing area:** 25 mm left/right, starts 48 mm from the top on page 1, ends 30 mm from the bottom. When printing on pre-printed sheets, use the Word template's margins.

## Fill before printing

- **[Company legal name]**: Solvexo LLC or i9 Experts (Pvt) Ltd (the open decision from the partner programme).
- Street address, phone, **NTN**, registered office.

Edit them in `letterhead.html` (print) and `make_docx.py` (Word), then run `node render.js` and `python3 make_docx.py`.
