# ERP-23 – Import order and reconciliation

## Source
- Source database: `uth_canteen_erp13_test`.
- Do not use `uth_canteen_erp22_sandbox`: it contains a negative-stock test artifact from ERP-22.
- All amounts are fictional DEMO VND values.

## Recommended import order
1. `suppliers.csv` – import supplier contacts first. Match existing suppliers by VAT and External ID mapping; do not create duplicates.
2. `products.csv` – contains the existing 20 UTH POS products copied from the project's current import file. The Service Fee product is intentionally excluded.
3. Resolve purchase-only raw material products before importing purchase orders. Existing verified External IDs include ST25, pho noodle, condensed milk and vegetable mix. Products with Odoo template IDs 73–77 have no verified External ID in the source database; their `erp23_product_*` values are handoff source keys, not Odoo External IDs.
4. `opening_inventory.csv` – apply only to `WH/Tồn kho` after confirming product mapping and UoM. Quantities are the verified source snapshot, not cumulative receipts.
5. `purchase_orders.csv` and `purchase_order_lines.csv` – import only after supplier/product mappings are approved. Preserve PO number as the natural reference. Confirm whether TV1 wants draft/confirmed documents recreated or historical documents retained as reference.

## Receipt status interpretation
- `done`: received and completed.
- `assigned`: reserved/ready but not completed; do not count as received.
- P00005: 1 of 2 Units of condensed milk received; backorder `WH/IN/00010` remains assigned.
- P00006–P00008: receipts remain assigned and are not counted as received.
- P00009: draft; excluded from confirmed purchase totals.

## Reconciliation
See `reconciliation.csv`. Confirmed P00001–P00008 total: 12,250,000 VND. P00009 is draft and has zero total.

## Important limitations
- `products.csv` and `suppliers.csv` are copied from the project's existing import files; they are not a fresh Odoo export.
- The purchase-order source keys are stable ERP-23 handoff identifiers, not existing Odoo External IDs.
- Product template IDs 73–77 have no verified External IDs. TV1 must map or create these records before importing related PO lines.
- Some proposed raw-material demo records differ from actual Odoo product names, brands or UoMs. Do not automatically map them.
- Standard costs shown in `opening_inventory.csv` are the source database's current company cost values; they are not supplier quotations or PO unit prices.
- **REC-14 – REVIEW_REQUIRED:** the source standard costs materially differ from confirmed PO unit prices: ST25 240,000 vs 27,000 VND/kg; fresh pho noodles 180,000 vs 22,000 VND/kg; condensed milk 11,200,000 vs 1,180,000 VND/Unit. Do not use these standard costs for opening inventory valuation or integration valuation until Finance/Accounting investigates and confirms the correct costs. The source snapshot values have not been modified.
- Supplier names in `purchase_orders.csv` are aligned with `suppliers.csv`; An Sáng uses the canonical name `Công ty Thực phẩm An Sáng UTH` and VAT `DEMO-VAT-0001`.
- This package is a handoff dataset for integration testing, not an instruction to blindly import all historical records into a live database.
