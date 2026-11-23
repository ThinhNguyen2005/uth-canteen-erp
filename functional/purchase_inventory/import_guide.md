# ERP-16 – Odoo CSV Import Guide

## 1. Files

- `products.csv`: 20 POS products, imported into `product.template`.
- `suppliers.csv`: 5 supplier contacts, model `res.partner`.

Both files use UTF-8 encoding and stable External IDs.

## 2. Product data

- Total: 20 POS products.
- All 20 products have unique internal references (SKU).
- All products use the `__import__` External ID namespace.
- All products have sales prices and are enabled for POS.
- Product type: `consu`.
- Cost prices are not included because recipe and ingredient costing has not been established.

## 3. Import products

1. Open Inventory > Products.
2. Select Import Records.
3. Upload `products.csv`.
4. Map External ID, Internal Reference, Name, Product Type, Can be Sold, Sales Price, Unit of Measure and Available in POS.
5. Test the import, then import the records.
6. Verify the 20 products in the Products list.

## 4. Import suppliers

1. Open Contacts.
2. Select Import Records.
3. Upload `suppliers.csv`.
4. Map External ID, Name, Supplier Rank, Customer Rank, Email, Phone, Street, City and VAT.
5. Test the import, then import the records.
6. Verify that exactly 5 supplier contacts exist.

## 5. Import verification

Product import:
- 20 product templates imported successfully.
- 20 unique SKUs.
- 20 products enabled in POS.
- Repeated product import did not increase the product count.

Supplier import:
- 5 supplier records imported successfully.
- External IDs use the `__import__` namespace.

## 6. Notes

- Product and supplier records are demonstration data for UTH Canteen ERP.
- Supplier contact details are fictional.
- Product cost and recipe costing are not included in this import scope.
