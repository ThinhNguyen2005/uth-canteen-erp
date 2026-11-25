# ERP-15 – Purchase and Inventory Process (AS-IS / TO-BE)

**Owner:** TV2 – Purchase & Inventory
**Status:** Draft – Pending TV1 review
**Scope:** Purchase, Receipt, Stock, Short Receipt and Supplier Return
**Target system:** Odoo

---

## 1. Objective

Describe the purchasing and warehouse receiving process for the UTH Canteen ERP project, from requesting a quotation to receiving goods and updating stock.

The process aims to:
- Ensure purchases are approved before ordering.
- Track ordered and actually received quantities.
- Maintain accurate inventory records.
- Handle shortages, damaged goods and supplier returns.
- Provide traceability for purchase and stock operations.

## 2. AS-IS – Current Process (To Be Confirmed)

**Important:** The following is a preliminary assumption for discussion. The actual current process must be confirmed by TV1 or the canteen's business representative.

| Step | Assumed current activity | Potential limitation |
|---|---|---|
| 1 | Staff identify ingredients that need replenishment | Reorder decisions may depend on manual stock checks |
| 2 | Staff contact suppliers to request prices and availability | Quotations may be stored in messages or separate documents |
| 3 | The responsible person confirms the purchase | Approval evidence may not be centralized |
| 4 | Supplier delivers goods to the canteen | Actual quantities and quality must be checked manually |
| 5 | Staff record received goods | Ordered and received quantities may be difficult to compare |
| 6 | Staff update stock records | Delayed updates can cause stock discrepancies |
| 7 | Shortages or damaged goods are discussed with suppliers | Follow-up and return records may be fragmented |

### AS-IS items requiring confirmation

- Who is authorized to request and approve purchases?
- Is there a purchase budget or approval threshold?
- How are supplier quotations compared?
- How are shortages and damaged goods currently recorded?
- Who is responsible for stock adjustments?

## 3. TO-BE – Proposed Odoo Process

### 3.1 Request for Quotation (RFQ)

1. The purchasing staff identifies a replenishment requirement.
2. Create an RFQ in Odoo Purchase.
3. Select the supplier and add products, quantities and expected prices.
4. Review the supplier quotation, delivery lead time and payment terms.
5. Submit the RFQ for approval according to the agreed authorization rules.

**Output:** RFQ with supplier and product details.

### 3.2 Purchase Order (PO)

1. Review and approve the RFQ.
2. Confirm the RFQ to create a Purchase Order.
3. Verify the supplier, ordered quantities, prices and planned delivery.
4. Odoo generates an incoming receipt operation.

**Output:** Confirmed PO and incoming receipt.

### 3.3 Receipt

1. Open the incoming receipt linked to the PO.
2. Check delivered products, actual quantities and product condition.
3. Enter the quantities actually received.
4. Record lot/serial information if applicable.
5. Validate the receipt when the physical check is complete.
6. If the delivery is incomplete, create a backorder for the remaining quantity when the supplier is expected to deliver it later.
7. If the remaining quantity is cancelled, do not create a backorder for that quantity.

**Output:** Validated receipt and updated received quantities.

### 3.4 Stock

1. After receipt validation, verify the products in the appropriate internal stock location.
2. Check on-hand quantities in Odoo Inventory.
3. Investigate discrepancies between expected and actual quantities.
4. Use an inventory adjustment only when a physical count identifies a stock difference.
5. Record the reason and approval for material adjustments.

**Output:** Updated stock balance and traceable inventory records.

### 3.5 Supplier Return (When Applicable)

1. Identify products that are damaged, incorrect or rejected.
2. Open the validated receipt and use the Return operation.
3. Enter the quantity to return and the return reason.
4. Confirm the return transfer.
5. Validate the outgoing return operation after goods physically leave the warehouse.
6. Follow up with the supplier for replacement, credit note or refund as agreed.

**Output:** Validated return transfer and documented supplier follow-up.

## 4. Business Rules

| Rule | Description |
|---|---|
| BR-01 | A PO must be confirmed before goods are expected through the normal purchasing flow |
| BR-02 | Received quantity must reflect the physical quantity accepted |
| BR-03 | A shortage must not be recorded as fully received |
| BR-04 | A backorder is used only when the remaining quantity is expected later |
| BR-05 | Cancelled remaining quantities must not be included in available stock |
| BR-06 | Inventory adjustments require a physical count and a reason |
| BR-07 | Supplier returns must reference the original receipt where applicable |
| BR-08 | Only authorized users may approve purchases and validate restricted operations |

## 5. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Requester / Canteen staff | Identify material requirements |
| Purchasing staff | Prepare RFQs, communicate with suppliers and create POs |
| Purchasing approver | Review and approve purchases |
| Warehouse staff | Inspect deliveries, process receipts and returns |
| Inventory controller | Review stock discrepancies and adjustments |
| TV1 / Business reviewer | Validate the proposed business process |

## 6. Odoo Records and Evidence

The following records should be used as evidence during testing:

- RFQ reference
- Purchase Order reference
- Incoming receipt reference
- Backorder reference, if applicable
- Return transfer reference, if applicable
- Inventory adjustment reference
- Product on-hand quantity before and after the operation

## 7. Assumptions and Pending Decisions

- Approval levels and purchase thresholds must be confirmed by TV1.
- Supplier prices and purchasing terms must use approved business data.
- The stock location and warehouse structure must follow the project's agreed configuration.
- Backorder handling must be confirmed with the business representative.
- Accounting treatment for supplier returns, refunds and credit notes is outside this document's operational scope and requires the responsible team to validate it.
- This document describes a proposed workflow; it does not claim that all approval rules have already been configured in Odoo.
