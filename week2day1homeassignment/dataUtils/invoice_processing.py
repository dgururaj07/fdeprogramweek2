
# ==========================================
# Home Assignment: Invoice Processing
# Steps 1 to 4
# ==========================================

invoices = [
    {"invoice_id": "INV-101", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
    {"invoice_id": "INV-102", "vendor": "xyz corp", "amount": 142500, "status": "pending", "date": "2026-09-05"},
    {"invoice_id": "INV-101", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
    {"invoice_id": "INV-103", "vendor": "Globex", "amount": -550000, "status": "PENDING", "date": "2026-09-07"},
    {"invoice_id": "INV-104", "vendor": "ABC Ltd ", "amount": 62000, "status": "PAID", "date": "2026-09-08"},
    {"invoice_id": "INV-102", "vendor": "XYZ Corp", "amount": 150000, "status": "PENDING", "date": "2026-09-12"},
    {"invoice_id": "INV-105", "vendor": "Globex", "amount": 550000, "status": "PENDING", "date": "2026-09-09"},
    {"invoice_id": "INV-106", "vendor": "Initech", "amount": None, "status": "PENDING", "date": "2026-09-15"},
    {"invoice_id": "INV-107", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
]

payments = [
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-104", "paid": 60000},
    {"invoice_id": "INV-109", "paid": 12000},
]


# Preserve original indexes for reporting
original_indexes = list(range(len(invoices)))


# ==========================================
# STEP 1: Normalize invoice data
# ==========================================

print("\n========== STEP 1: NORMALIZATION ==========")

missing_amounts = []

for index in range(len(invoices)):

    invoices[index]["vendor"] = (
        invoices[index]["vendor"].strip().title()
    )

    invoices[index]["status"] = (
        invoices[index]["status"].upper()
    )

    if invoices[index]["amount"] is None:
        missing_amounts.append(index)

        print(
            f"Index {index}: "
            f'{invoices[index]["invoice_id"]} '
            f"has amount=None"
        )

print("\nNormalized invoices:")

for invoice in invoices:
    print(invoice)

print("\nIndexes with missing amounts:", missing_amounts)


# ==========================================
# STEP 2: Find and remove exact duplicates
# ==========================================

print("\n========== STEP 2: EXACT DUPLICATES ==========")

invoice_groups = {}

for index in range(len(invoices)):

    invoice = invoices[index]

    # Create a key using every field
    key = tuple(invoice.values())

    if key not in invoice_groups:
        invoice_groups[key] = []

    invoice_groups[key].append(index)


# Keep only duplicate groups
exact_dupes = {
    key: indexes
    for key, indexes in invoice_groups.items()
    if len(indexes) > 1
}

print("Exact duplicate groups:")

for key, indexes in exact_dupes.items():
    print(key, "->", indexes)


# Collect indexes to remove, preserving the first row
duplicate_indexes_to_remove = set()

for indexes in exact_dupes.values():
    duplicate_indexes_to_remove.update(indexes[1:])


# Filter invoices and original indexes together
invoices = [
    invoice
    for index, invoice in enumerate(invoices)
    if index not in duplicate_indexes_to_remove
]

original_indexes = [
    index
    for index in original_indexes
    if index not in duplicate_indexes_to_remove
]

print("\nInvoices after removing exact duplicates:")

for invoice in invoices:
    print(invoice)

print("Total invoices remaining:", len(invoices))


# ==========================================
# STEP 3: Find suspected duplicates
# ==========================================

print("\n========== STEP 3: SUSPECTED DUPLICATES ==========")

suspected_dupes = []

for i in range(len(invoices)):

    for j in range(i + 1, len(invoices)):

        invoice1 = invoices[i]
        invoice2 = invoices[j]

        # Skip invoices with missing amounts
        if (
            invoice1["amount"] is None
            or invoice2["amount"] is None
        ):
            continue

        same_vendor = (
            invoice1["vendor"] == invoice2["vendor"]
        )

        same_amount = (
            invoice1["amount"] == invoice2["amount"]
        )

        same_date = (
            invoice1["date"] == invoice2["date"]
        )

        different_ids = (
            invoice1["invoice_id"]
            != invoice2["invoice_id"]
        )

        if (
            same_vendor
            and same_amount
            and same_date
            and different_ids
        ):

            pair = (
                invoice1["invoice_id"],
                invoice2["invoice_id"]
            )

            suspected_dupes.append(pair)

            print(f"({pair[0]} ~ {pair[1]})")


if not suspected_dupes:
    print("No suspected duplicates found.")

print("Total suspected duplicate pairs:", len(suspected_dupes))
print("Invoices remaining:", len(invoices))


# ==========================================
# STEP 4: Process credit notes
# ==========================================

print("\n========== STEP 4: CREDIT NOTES ==========")

matched_credit_indexes = set()

for i in range(len(invoices)):

    negative_invoice = invoices[i]

    # Only process negative invoices
    if (
        negative_invoice["amount"] is None
        or negative_invoice["amount"] >= 0
    ):
        continue

    # Skip an already matched invoice
    if i in matched_credit_indexes:
        continue

    partner_found = False

    for j in range(len(invoices)):

        if i == j:
            continue

        positive_invoice = invoices[j]

        # Partner must have a positive amount
        if (
            positive_invoice["amount"] is None
            or positive_invoice["amount"] <= 0
        ):
            continue

        same_vendor = (
            negative_invoice["vendor"]
            == positive_invoice["vendor"]
        )

        same_absolute_amount = (
            abs(negative_invoice["amount"])
            == positive_invoice["amount"]
        )

        if same_vendor and same_absolute_amount:

            # Mark both invoices as cancelled
            negative_invoice["status"] = "CANCELLED"
            positive_invoice["status"] = "CANCELLED"

            matched_credit_indexes.add(i)
            matched_credit_indexes.add(j)

            print(
                f"{original_indexes[i]} <-> "
                f"{original_indexes[j]}"
            )

            print(
                f'{negative_invoice["invoice_id"]}: '
                f'{negative_invoice["status"]}'
            )

            print(
                f'{positive_invoice["invoice_id"]}: '
                f'{positive_invoice["status"]}'
            )

            partner_found = True
            break

    if not partner_found:
        print(
            "No positive partner found for "
            f'{negative_invoice["invoice_id"]} '
            f"(original index {original_indexes[i]})"
        )


print("\nInvoices after credit-note processing:")

for index, invoice in zip(original_indexes, invoices):
    print(f"Original index {index}: {invoice}")



# ==========================================
# STEP 5: Reconcile payments
# ==========================================

print("\n========== STEP 5: PAYMENT RECONCILIATION ==========")

# 1. Group invoices by invoice_id
invoice_groups_by_id = {}

for invoice in invoices:
    invoice_id = invoice["invoice_id"]

    if invoice_id not in invoice_groups_by_id:
        invoice_groups_by_id[invoice_id] = []

    invoice_groups_by_id[invoice_id].append(invoice)


# 2. Sum payments for each invoice_id
payment_totals = {}

for payment in payments:
    invoice_id = payment["invoice_id"]

    if invoice_id not in payment_totals:
        payment_totals[invoice_id] = 0

    payment_totals[invoice_id] += payment["paid"]


print("\nTotal payments by invoice:")

for invoice_id, total_paid in payment_totals.items():
    print(f"{invoice_id}: Rs {total_paid:,.2f}")


# 3. Reconcile payments against invoices
print("\nReconciliation results:")

matched_payment_ids = set()

for invoice_id, invoice_group in invoice_groups_by_id.items():

    # Exclude invoices with missing amounts
    valid_invoices = [
        invoice
        for invoice in invoice_group
        if invoice["amount"] is not None
    ]

    # Exclude cancelled invoices from reconciliation
    active_invoices = [
        invoice
        for invoice in valid_invoices
        if invoice["status"] != "CANCELLED"
    ]

    if not active_invoices:
        print(f"{invoice_id}: Excluded (missing or cancelled)")
        continue

    # Flag invoice IDs associated with multiple active rows
    if len(active_invoices) > 1:
        print(
            f"{invoice_id}: CONFLICT - multiple active "
            "invoices share this ID; manual review required"
        )
        continue

    invoice = active_invoices[0]
    invoice_amount = invoice["amount"]
    total_paid = payment_totals.get(invoice_id, 0)

    # Track payment IDs that match an active invoice
    if invoice_id in payment_totals:
        matched_payment_ids.add(invoice_id)

    difference = invoice_amount - total_paid

    if total_paid == 0:
        result = "UNPAID"

    elif total_paid < invoice_amount:
        result = "PARTIALLY PAID"

    elif total_paid == invoice_amount:
        result = "PAID"

    else:
        result = "OVERPAID"

    print(f"\nInvoice ID: {invoice_id}")
    print(f"Invoice amount: Rs {invoice_amount:,.2f}")
    print(f"Total paid: Rs {total_paid:,.2f}")
    print(f"Balance (invoice amount - paid): Rs {difference:,.2f}")
    print(f"Status: {result}")


# 4. Identify payments with no matching active invoice
print("\nUnmatched payments:")

unmatched_found = False

for invoice_id, total_paid in payment_totals.items():

    invoice_group = invoice_groups_by_id.get(invoice_id, [])

    active_invoices = [
        invoice
        for invoice in invoice_group
        if invoice["amount"] is not None
        and invoice["status"] != "CANCELLED"
    ]

    if not active_invoices:
        print(
            f"{invoice_id}: Rs {total_paid:,.2f} "
            "has no eligible invoice"
        )
        unmatched_found = True

    elif len(active_invoices) > 1:
        print(
            f"{invoice_id}: Rs {total_paid:,.2f} "
            "cannot be reconciled because the invoice ID is ambiguous"
        )
        unmatched_found = True

if not unmatched_found:
    print("No unmatched payments found.")
