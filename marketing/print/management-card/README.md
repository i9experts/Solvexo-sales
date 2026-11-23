# Management Business Cards (F3)

Premium card for management (founder, directors, partnership leads), used in partner and investor meetings. Different from the rep cards on purpose: dark and understated.

- **Front (dark):** Solvexo logo (white wordmark), name, title in coral capitals, phone, email, solvexo.store, optional LinkedIn; terracotta strip on the right edge.
- **Back (terracotta):** the Solvexo icon on a white tile, "CREATE · SELL · MANAGE · GROW", solvexo.store, and a **"SAVE MY CONTACT" QR**: a vCard, so scanning it offers to save the person (name, company, title, phone, email, website) straight into the phone's contacts.
- **Spot UV:** a separate mask file per person, with gloss varnish on the front logo and the back icon tile (black = varnish).

## How to make cards

1. Fill `managers.csv`: `name, title, phone (as printed, e.g. +92 300 1234567), email, whatsapp (optional), linkedin (optional)`.
2. `python3 make_cards.py` (needs `pip install segno pypdf`, Node + Playwright).
3. Per person in `output/`: `<name>_print.pdf` (front, back), `<name>_spotuv.pdf` (masks), previews.
4. Scan the QR: the phone should offer "Add contact" with the right details.

`output/` is git-ignored (personal contact details).

## Print specs

- 3.5 × 2 in (88.9 × 50.8 mm) + 3 mm bleed; text 4 mm inside the trim.
- **400 gsm matte (soft-touch laminate if available) + spot UV** using the mask file. 200 per person.
- Ask for a proof: dark backgrounds show colour shifts more easily.
