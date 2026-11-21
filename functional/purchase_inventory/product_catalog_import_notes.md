# Product Catalog – Import Notes (Odoo 20.0)

## Files and intended use

- `product_catalog.csv`: TV2 master catalog and cross-team reconciliation file. It contains business metadata and pending decisions; **do not import this file directly**.
- `product_import_raw_materials_template.csv`: Odoo-import-shaped draft for the 10 raw-material records only. Use only in a disposable/test database after UoM and category checks.
- `supplier_pricelist_mapping_template.csv`: workpaper for recording the actual supplier, quoted purchase price, supplier UoM, minimum quantity, lead time, and quotation reference. It is not an Odoo import file.
- The 13 POS products are already declared in `addons/canteen_management/demo/canteen_demo_data.xml`; do not import them again as new products.

## Mapping in the raw-material import draft

| CSV column | Odoo model/field | Meaning |
|---|---|---|
| `id` | External ID | Stable XML ID for import/update |
| `name` | `product.template.name` | Product name |
| `default_code` | `product.template.default_code` | Internal Reference / SKU |
| `type` | `product.template.type` | `consu` (Goods) |
| `purchase_ok` | `product.template.purchase_ok` | Purchase enabled |
| `sale_ok` | `product.template.sale_ok` | Sales disabled for raw materials |
| `list_price` | `product.template.list_price` | 0 for non-sale raw materials |
| `uom_id/id` | `product.template.uom_id` | Stock unit of measure by XML ID |
| `is_storable` | `product.template.is_storable` | Enable stock quantity tracking |
| `available_in_pos` | `product.template.available_in_pos` | Raw materials not shown as POS products |
| `categ_id/id` | `product.template.categ_id` | Standard Goods category |

## Important limitations before import

1. `standard_price` is intentionally omitted from the import draft. The numbers in `demo_raw_materials.csv` are demo cost values, not verified supplier quotations.
2. No supplier is assigned because the existing demo supplier file does not explicitly map suppliers to the ten products. Do not guess the mapping. Fill `supplier_pricelist_mapping_template.csv` from actual supplier information.
3. The `uom.product_uom_unit` value is generic. For condensed milk (carton of 48 cans) and eggs (tray of 30), confirm whether stock is counted by carton/tray or by can/egg before import. For rice sold by bag but counted by kg, confirm the supplier purchase unit and conversion.
4. The standard Odoo 20 product category XML ID used in the template is `product.product_category_goods`. The earlier source file's `product.product_category_all` should not be assumed to exist in Odoo 20.
5. POS products are retained for reuse from XML. Their actual `purchase_ok`, `is_storable`, costs, recipe/BOM consumption and vendor settings still need operational confirmation.
6. This draft does not prove import success. Test it on a disposable Odoo database, verify the import mapping preview, and inspect the created records before accepting it.

## Odoo 20 source references

- Product template model: https://github.com/odoo/odoo/blob/20.0/addons/product/models/product_template.py
- Supplier pricelist model: https://github.com/odoo/odoo/blob/20.0/addons/product/models/product_supplierinfo.py
- POS product fields: https://github.com/odoo/odoo/blob/20.0/addons/point_of_sale/models/product_template.py
- Standard Goods category data: https://github.com/odoo/odoo/blob/20.0/addons/product/data/product_data.xml
