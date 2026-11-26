"""Test a synthetic 10% quantity-limited pricelist through the Odoo ORM."""
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
assert not env["product.pricelist"].search_count([("name", "=", "KAN152 Student Test")])
product_a = env["product.product"].search([("default_code", "=", "KAN151-A")], limit=1)
product_b = env["product.product"].search([("default_code", "=", "KAN151-B")], limit=1)
assert product_a and product_b
pricelist = env["product.pricelist"].create({
    "name": "KAN152 Student Test", "currency_id": env.company.currency_id.id,
    "item_ids": [Command.create({"applied_on": "0_product_variant", "product_id": product_a.id, "min_quantity": 2, "compute_price": "discount", "price_discount": 10})],
})
prices = [pricelist._get_product_price(product_a, 1), pricelist._get_product_price(product_a, 2), pricelist._get_product_price(product_b, 2)]
assert prices == [20000, 18000, 35000], prices
env.cr.commit()
print("KAN152_PRICELIST", pricelist.id, "prices_A1_A2_B2", prices)
