# POS Cheat Sheet (E2): A5 landscape, laminated

Lives at the till for the seller's staff. One per live seller (more for shops with several counters).

- **Front: 8 everyday tasks** as tiles, each with 3 short steps and an Urdu line: Start your shift · Make a sale · Discount or coupon · Add the customer · Take payment (cash/change, card, split) · Receipt · Hold a sale · End your shift.
- **Back:** Every day at the till (morning / every sale / online orders / evening) · If something goes wrong (wrong item, sale completed by mistake, product not found, internet down) · Keep it safe (never share your PIN, log out) · write-in Manager and Solvexo contact · QR to the full POS manual (solvexo.store/manuals, EN/UR).
- **Size:** A5 landscape (210 × 148 mm) + 3 mm bleed. **300 gsm, laminated both sides** (wet hands at the counter). Optional: hole-punch a corner to hang it by the register.
- Rebuild: `node render.js` → `output/pos-cheat-sheet.pdf` (page 1 front, page 2 back) + PNG previews.

## Check before printing

Button names (*Discount*, *Customer*, *Pay*, *Hold*, *held sales*, *shift summary*, *start/end shift*, opening cash) are based on the POS feature list (sale, discounts/coupons, customer lookup, cash change, split payments, hold sales, receipts, shift summary, PIN login). **Walk through the live POS once with this sheet** and correct any label that differs. The "internet is down" tip assumes the POS needs a connection; confirm, and change it if offline sales are supported.
