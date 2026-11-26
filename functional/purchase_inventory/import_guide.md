# ERP-16 – Odoo CSV Import Guide

## 1. Files and encoding

- `products.csv`: 20 POS products imported into the **Product** model (`product.template`).
- `suppliers.csv`: 5 supplier contacts imported into `res.partner`.
- CSV files are UTF-8 without BOM.
- Preserve the External IDs already assigned to existing records.

## 2. Product External IDs and target model

The current test database `uth_canteen_erp13_test` contains all 20 products as `product.template` records. Their External IDs are in the `__import__` namespace, for example:

- `__import__.product_rice_chicken`
- `__import__.product_rice_broken`
- `__import__.product_drink_coffee_milk`
- `__import__.product_fastfood_burger`

The CSV retains the exact `__import__.*` IDs for all 20 existing products. Do not replace the first 13 IDs with `canteen_management.*`: those XML IDs are not present in the current database, and the corresponding XML records are not evidence that they have been loaded.

Import `products.csv` from the Products list using the Product model (`product.template`), not Product Variants (`product.product`). The External ID must resolve to the existing template so the import updates that record rather than creating another product.

## 3. Product data contract

- Total: 20 products.
- All 20 products have unique internal references (SKU).
- All products use type `consu`, are saleable, and are enabled in POS.
- `available_in_pos` is supported by the current database.
- This database does not contain `canteen_published` or `canteen_category` on either `product.template` or `product.product`; these fields are intentionally excluded from this CSV.
- Product cost and recipe costing are not included because approved costing data has not been established.

## 4. Import products

1. Open Products (model `product.template`) in Odoo.
2. Select Import Records and upload `products.csv`.
3. Map External ID, Internal Reference, Name, Product Type, Can be Sold, Sales Price, Unit of Measure and Available in POS.
4. Confirm the target model is Product (`product.template`).
5. Test the import. Confirm all 20 `__import__.*` External IDs resolve to existing templates.
6. Only proceed with Import if the preview resolves existing records and does not indicate creation of additional products.
7. After import, verify 20 unique SKUs and unchanged product count.

## 5. Import suppliers

1. Open Contacts and select Import Records.
2. Upload `suppliers.csv`.
3. Map External ID, Name, Supplier Rank, Customer Rank, Email, Phone, Street, City and VAT.
4. Test the import, then import only after confirming the five IDs resolve to the intended contacts.
5. The supplier IDs intentionally match the bare IDs in `demo_suppliers.csv`, without an `__import__.` prefix.

## 6. Re-import and duplicate checks

- Re-importing the product file must update the same 20 product templates and must not increase the product count.
- Re-importing the supplier file must update the same five contacts and must not create duplicates.
- Verify all 20 product External IDs resolve to `product.template`.
- Verify the five supplier External IDs resolve to the same contacts referenced by `demo_suppliers.csv`.

## 7. Data notes

- Supplier contact details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this import scope.
