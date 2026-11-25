# ERP-15 – Purchase and Inventory Test Cases

**Owner:** TV2 – Purchase & Inventory
**Status:** Executed – Pending TV1 review
**Environment:** Odoo test database
**Test data:** Use approved products and suppliers from ERP-13 / ERP-14 after integration.

---

## TC-01 – Normal Purchase and Full Receipt

**Status:** PASS

**Objective:** Verify that a normal purchase updates inventory correctly.

**Preconditions:**
- A valid supplier exists.
- A storable product exists.
- The product has a valid purchase unit of measure.
- The user has permission to create and confirm purchase orders and validate receipts.

**Test data (example):**

| Field | Value |
|---|---|
| Product | Gạo thơm ST25 Thượng hạng (Bao 25kg) |
| Supplier | Công ty Thực phẩm An Sáng UTH |
| Ordered quantity | 100 |
| Received quantity | 100 |
| Receipt condition | Accepted |

**Steps:**

1. Open Purchase → Requests for Quotation.
2. Create an RFQ and select the supplier.
3. Add the product with quantity 100 and an agreed price.
4. Save and confirm the RFQ to create a PO.
5. Open the incoming receipt generated from the PO.
6. Verify the product and expected quantity.
7. Confirm that the physical delivery contains 100 accepted units.
8. Set the received quantity to 100.
9. Validate the receipt.
10. Open the product's inventory information and verify the stock increase.

**Expected results:**
- RFQ is saved successfully.
- PO is created after confirmation.
- An incoming receipt is generated.
- The receipt is validated with 100 units received.
- No backorder is required.
- On-hand stock increases by 100 units, assuming no other stock movements.

**Evidence:**
- Purchase Order: P00001
- Receipt: WH/IN/00001
- Database verification: stock picking state = done, received quantity = 100 kg, on-hand quantity = 100 kg.

## TC-02 – Partial Receipt / Short Delivery

**Objective:** Verify that a delivery shortage is recorded accurately and the remaining quantity is handled correctly.

**Preconditions:**
- A valid supplier and storable product exist.
- A confirmed PO exists.

**Test data (example):**

| Field | Value |
|---|---|
| Ordered quantity | 100 |
| Physically received quantity | 80 |
| Remaining quantity | 20 |
| Remaining quantity expected later | Yes |

**Steps:**

1. Create and confirm an RFQ for 100 units.
2. Open the incoming receipt.
3. Inspect the physical delivery and confirm that only 80 units are accepted.
4. Enter 80 as the received quantity.
5. Validate the receipt.
6. When prompted, choose to create a backorder for the remaining 20 units.
7. Open the original PO and verify the received and remaining quantities.
8. Open the backorder and verify that it contains the remaining 20 units.
9. Verify the product's on-hand quantity.

**Expected results:**
- The original receipt records 80 received units.
- The remaining 20 units are not incorrectly added to stock.
- A backorder is created for 20 units.
- The PO reflects the partial receipt and outstanding quantity.
- On-hand stock increases by 80 units, assuming no other stock movements.

**Alternative:** If the supplier confirms that the remaining 20 units will not be delivered, cancel the remaining quantity instead of creating a backorder. Verify that no backorder remains open.

**Evidence to capture:**
- PO reference.
- Original receipt reference.
- Backorder reference and quantity.
- Product on-hand quantity.

---

## TC-03 – Inventory Adjustment

**Objective:** Verify that a physical stock discrepancy can be recorded and reconciled.

**Preconditions:**
- A storable product exists in an internal stock location.
- The user has permission to perform inventory counts and validate adjustments.

**Test data (example):**

| Field | Value |
|---|---|
| System quantity before count | 200 kg |
| Physical counted quantity | 197 kg |
| Difference | -3 |

**Steps:**

1. Open Inventory and locate the product in the internal stock location.
2. Record the current on-hand quantity of 200 kg.
3. Start an inventory count / inventory adjustment for the product.
4. Enter the physically counted quantity of 197 kg.
5. Review the calculated difference of -3 kg.
6. Enter a reason or reference for the discrepancy if the configured workflow supports it.
7. Validate / apply the inventory adjustment.
8. Reopen the product inventory information.
9. Verify the updated on-hand quantity.

**Expected results:**
- The system identifies a difference of -3 units.
- The adjustment is recorded and validated.
- On-hand stock becomes 197 kg, assuming no concurrent stock movements.
- The adjustment can be traced through its inventory record or stock move.

**Evidence to capture:**
- Inventory adjustment reference.
- Product and location.
- Quantity before count, counted quantity and difference.
- Updated on-hand quantity after validation.

---

## Optional Scenario – Supplier Return

**Objective:** Verify the operational flow for returning damaged or incorrect goods.

**Preconditions:**
- A receipt has been validated.
- Some received units are identified as damaged or rejected.

**Test data (example):**
- Original accepted receipt: 100 units.
- Quantity to return: 5 units.

**Steps:**

1. Open the validated incoming receipt.
2. Use the Return operation.
3. Enter the quantity of 5 units and the return reason.
4. Confirm the return operation.
5. Validate the outgoing return transfer after the goods physically leave the warehouse.
6. Verify the resulting stock quantity and return record.
7. Record the supplier's replacement, refund or credit-note agreement separately.

**Expected results:**
- A return operation references the original receipt.
- The returned quantity is 5 units.
- Stock decreases by 5 units after the return is validated, assuming no other stock movements.
- The return reason and supplier follow-up are documented.

**Note:** This optional scenario does not replace the three mandatory acceptance test cases.

---

## Test Execution Summary

| Test case | Result | Odoo reference | Evidence |
|---|---|---|---|
| TC-01 – Normal purchase | PASS | P00001 / WH/IN/00001 | 100 kg received; 100 kg on-hand |
| TC-02 – Partial receipt | PASS | P00002 / WH/IN/00002 / WH/IN/00003 | 80 kg initial receipt; 20 kg backorder; both Done |
| TC-03 – Inventory adjustment | PASS | ST25 Physical Inventory | 200 kg before; 197 kg counted; -3 kg adjustment; 197 kg after |
| Optional – Supplier return | Not executed | Pending | Pending |

## Review Checklist

- [ ] AS-IS assumptions confirmed by business representative.
- [ ] TO-BE workflow reviewed by TV1.
- [x] TC-01 executed successfully in Odoo.
- [x] TC-02 executed successfully in Odoo.
- [x] TC-03 executed successfully in Odoo.
- [ ] Odoo references and screenshots attached.
- [ ] PR reviewed and approved.
- [ ] Jira updated with test results and evidence.
