# Window / Door Decal (B2): personalised per seller

A 6 × 6 inch decal on the shop's glass door or window. People passing by scan it to open the seller's own Solvexo store.

## How to make decals

1. Uses the same seller list as the tent card: `../tent-card/sellers.csv` (`store_name,subdomain`).
2. Run `python3 make_decals.py` (needs `pip install segno pypdf`, Node + Playwright, `pdfunite`).
3. In `output/` you get, per seller:
   - `<sub>_outside.pdf`: for **opaque white vinyl** stuck on the **outside** of the glass. Reads normally.
   - `<sub>_inside.pdf`: **mirrored**, for **clear vinyl** stuck on the **inside** of the glass and read through it. Protected from weather and cleaning.
   - `<sub>.png`: preview. With several sellers, `ALL_decals_outside.pdf` / `ALL_decals_inside.pdf` combine them.
4. **Scan each QR before printing**, and scan it again through the glass once fitted.

## Which version to use

| Situation | Use | Vinyl |
|---|---|---|
| Glass the owner can reach outside, little rain | `_outside` | Opaque white gloss vinyl + matte laminate |
| Shop front exposed to rain, dust or daily cleaning | `_inside` | Clear vinyl, printed mirrored, **with a white ink layer behind the colours** (ask the printer) so it isn't see-through |

## Print specs

- **Size:** 152.4 × 152.4 mm (6 in) + 3 mm bleed = 158.4 mm square. Straight cut, or 8 mm rounded corners.
- **Placement:** at eye level (about 1.2–1.5 m), near the door handle, away from glare. Keep the QR area clean.
- **QR:** about 62 mm wide with high error correction (Q), so it still scans with some glare or dirt. Links carry `utm_source=windowdecal`.
- **Content:** no delivery or payment promises (they differ per seller).
