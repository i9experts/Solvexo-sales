# Rep Visiting Cards (A5): personalised per rep

Standard 3.5 × 2 in card, double-sided.

- **Front (the person):** terracotta side rail, Solvexo logo, rep's name (+ optional Urdu name), title, WhatsApp/phone, optional email, solvexo.store.
- **Back (the brand):** terracotta with the logo, "Your shop counter and online store. One app.", the tagline, and a **"WhatsApp me" QR** that opens a chat with that rep, pre-filled with *"Salam, I'd like a Solvexo demo for my shop."*

## How to make cards

1. Fill `reps.csv` (one row per rep): `name, name_ur (optional), title, phone (as printed), whatsapp (92 + 10 digits), email (optional)`.
2. Run `python3 make_cards.py` (needs `pip install segno`, Node + Playwright, `pdfunite`).
3. Print files are in `output/`: `<name>.pdf` (page 1 front, page 2 back), previews, and `ALL_rep_cards.pdf`.
4. **Scan each QR** before printing: it must open WhatsApp to the right rep's number.

`output/` is git-ignored because it contains staff phone numbers. Keep `reps.csv` to work numbers the reps have agreed to print.

## Print specs

- 3.5 × 2 in (88.9 × 50.8 mm) + 3 mm bleed; text 4 mm inside the trim.
- 350–400 gsm matte, double-sided; optional spot-UV on the back logo.
- 200 per rep to start.
