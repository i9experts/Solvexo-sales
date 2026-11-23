# Rep ID Card + Lanyard (A6): personalised per rep

Portrait CR80 card (the size of a bank card) on a lanyard. Builds trust at the shop: "who are you?" is answered, and the owner can **verify the rep in one scan**.

- **Front:** terracotta top with the Solvexo logo, rep photo, name (+ optional Urdu name), "AUTHORISED REPRESENTATIVE", ID number, valid-until date.
- **Back:** "Verify this representative", a QR that opens WhatsApp to the **office** with *"Verify Solvexo rep ID SVX-001"* pre-filled, the office phone, Urdu line *تصدیق کے لیے اس نمبر پر رابطہ کریں*, and "property of / if found, return to".

## How to make cards

1. **Edit `OFFICE` once** at the top of `make_ids.py`: company name, office phone (as printed), office WhatsApp (92 + 10 digits), address. **Use a number the office actually answers.** That is the whole point of the verification QR.
2. Put rep photos in `photos/` (passport style, plain background, 3:4 portrait, at least 600 × 800 px).
3. Fill `ids.csv`: `name, name_ur (optional), id_no (SVX-001…), valid_until, photo (file name)`.
4. Run `python3 make_ids.py`. Find the print files in `output/`: `<ID>.pdf` (page 1 front, page 2 back), previews, `ALL_id_cards.pdf`.
5. Scan each verification QR.

`output/` and `photos/` are git-ignored (staff photos and details).

## Print specs

- **Card:** CR80 PVC, 54 × 85.6 mm portrait, printed both sides, 2 mm bleed in the file (58 × 89.6 mm). **Slot punch top centre**; the top 12 mm is kept free of text for it.
- **Lanyard:** `render_lanyard.js` → `output/lanyard_20mm_tile.pdf`: 20 mm wide, 450 mm repeat, terracotta with the icon and SOLVEXO / SOLVEXO.STORE. Ask for a **safety breakaway clip** and a metal hook for the slot.
- 1 card + 1 lanyard per rep; reprint when the valid-until date passes or the rep leaves (collect the old card).
