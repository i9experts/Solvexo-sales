# Counter QR Tent Card (B1): personalised per seller

Stands on a live seller's counter. Their **customers** scan it to open the seller's own Solvexo store. Each card carries that seller's name and store link, with a small "Powered by Solvexo".

## How to make cards

1. Add one row per seller to `sellers.csv`:
   ```
   store_name,subdomain
   Al-Noor Mobiles,alnoor-mobiles
   ```
   `subdomain` is the part before `.solvexo.store` in their store link.
2. Run `python3 make_tent_cards.py` (needs `pip install segno`, Node + Playwright, and `pdfunite`).
3. Find the print files in `output/`: one PDF per seller, a PNG preview each, and `ALL_tent_cards.pdf` with all of them for the printer.
4. **Scan each QR before printing** to make sure it opens the right live store.

## Print and fold

- **Flat size:** 105 × 296 mm (two A6 faces) + 3 mm bleed = 111 × 302 mm. Small fold marks sit in the bleed at the centre line.
- **Stock:** 350 gsm matte card, single-sided. Matte laminate if possible (counters get wet hands).
- **Fold** along the centre line. The top half is printed upside down on purpose, so both faces read upright once folded.
- **Stability:** a two-panel tent can slide. Use a strip of double-sided tape inside the base, or slip the flat card into a clear A6 acrylic stand instead of folding it.

## Content rules

- The card is for the seller's customers, so the wording is about the shop: "Shop with us online, anytime".
- No delivery or payment promises on the card (they differ per seller). Add a line only if that seller confirms it.
- QR links carry `utm_source=tentcard` so store visits from the card can be counted.
