# ERP-23 – Purchase & Inventory Integration Handoff

This folder contains the TV2 handoff package for TV1 integration testing.

## Files
- `products.csv` – existing 20 UTH POS products from the project's current import dataset.
- `suppliers.csv` – existing 5 demo suppliers from the project's current import dataset.
- `opening_inventory.csv` – verified opening stock snapshot at `WH/Tồn kho`.
- `purchase_orders.csv` – 9 source PO headers (8 confirmed, 1 draft).
- `purchase_order_lines.csv` – 13 PO lines with stable ERP-23 source keys.
- `reconciliation.csv` – counts, totals, receipt status and known mapping gaps.
- `import_order.md` – import sequence, status interpretation and limitations.

## Source and safety
Source database: `uth_canteen_erp13_test`.
The ERP-22 sandbox is deliberately excluded because it contains a negative-stock test artifact.
All supplier and purchase values are fictional DEMO data in VND.

## Integration gate
Do not import purchase orders until TV1 confirms product and supplier mapping, especially products 73–77 which do not have verified Odoo External IDs. The `erp23_*` source keys are stable handoff identifiers only.