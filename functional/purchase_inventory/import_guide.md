# ERP-16 – Odoo CSV Import Guide

## 1. Files and encoding

- `products.csv`: 20 POS products imported into the **Product Variant** model (`product.product`).
- `suppliers.csv`: 5 supplier contacts imported into `res.partner`.
- All files are UTF-8 **without BOM**.
- CSV files use stable External IDs. Do not replace the canonical IDs of existing records.

## 2. Product External IDs and model

The first 13 POS products already exist in `addons/canteen_management/demo/canteen_demo_data.xml` as records of model `product.product`. Their CSV External IDs therefore use the exact module-qualified IDs from that XML:

- `canteen_management.product_rice_chicken` through the corresponding IDs listed in the XML.
- The remaining 7 newly added products use the `__import__` namespace.

**Important:** Import this file against `product.product` (Product Variants), not `product.template`. Importing the canonical `product.product` External IDs against a different model can fail to update the existing variants and may create duplicate product data.

Open the Product Variants list in Odoo, choose Import Records, upload `products.csv`, and verify the target model is Product Variant / `product.product` before importing.

## 3. Product data contract

- Total: 20 POS products.
- All 20 products have unique internal references (SKU).
- All products use type `consu`, are saleable, and are enabled in POS.
- All products have `canteen_published = True`.
- `canteen_category` uses only the categories already present in the canteen demo data: `rice`, `noodle`, `drink`, `snack`, `fastfood`.
- The first 13 External IDs exactly match the XML records in model `product.product`.
- Product cost and recipe costing are not included because approved costing data has not been established.

## 4. Import products

1. Open the Product Variants list (model `product.product`) in Odoo.
2. Select Import Records.
3. Upload `products.csv`.
4. Map External ID, Internal Reference, Name, Product Type, Can be Sold, Sales Price, Unit of Measure, Available in POS, Canteen Published and Canteen Category.
5. Confirm the target model is `product.product`.
6. Test the import first. Confirm the 13 canonical External IDs resolve to existing product variants; they must be updated, not duplicated.
7. Import, then verify 20 unique SKUs and the two canteen fields.

## 5. Import suppliers

1. Open Contacts.
2. Select Import Records.
3. Upload `suppliers.csv`.
4. Map External ID, Name, Supplier Rank, Customer Rank, Email, Phone, Street, City and VAT.
5. Test the import, then import the records.
6. Verify the five External IDs match the bare IDs used in `demo_suppliers.csv` (for example, `partner_supplier_an_sang`), without the `__import__.` prefix.

## 6. Re-import and duplicate checks

- Re-importing the product file must update the same 20 product variants and must not increase the number of records.
- Re-importing the supplier file must update the same five contacts and must not create duplicates.
- Verify the 13 existing product External IDs resolve to model `product.product`.
- Verify the five supplier External IDs resolve to the same contacts referenced by `demo_suppliers.csv`.

## 7. Data notes

- Supplier contact details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this import scope.
