import json

invoices=[
  {
    "invoice_id": 101,
    "vendor": "Meta",
    "amount": 95000,
    "status": "PENDING"
  },
  {
      "invoice_id": 101,
      "vendor": "Meta",
      "amount": 95000,
      "status": "PENDING"
    },
  {
    "invoice_id": 102,
    "vendor": "Google",
    "amount": 8000,
    "status": "PENDING"
  },
   {
      "invoice_id": 102,
      "vendor": "Google",
      "amount": 8000,
      "status": "PENDING"
    },
  {
    "invoice_id": 103,
    "vendor": "Meta",
    "amount": 6000,
    "status": "PAID"
  },
  {
    "invoice_id": 104,
    "vendor": "Google",
    "amount": 10000,
    "status": "unpaid"
  },
  {
    "invoice_id": 104,
    "vendor": "Google",
    "amount": 10000,
    "status": "unpaid"
  },
  {
    "invoice_id": 104,
    "vendor": "Fidelity",
    "amount": 10000,
    "status": "unpaid"
  }
]


vendor_totals={}

for invoice in invoices:
    vendor=invoice["vendor"]
    amount=invoice["amount"]
    vendor_totals[vendor]=vendor_totals.get(vendor,0)+amount

print(vendor_totals)

id_counts = {}
for invoice in invoices:
    invoice_id = invoice["invoice_id"]
    id_counts[invoice_id] = id_counts.get(invoice_id, 0) + 1

duplicate_invoices = [invoice for invoice in invoices if id_counts[invoice["invoice_id"]] > 1]

print(duplicate_invoices)

vendor_counts = {}
for invoice in invoices:
    vendor = invoice["vendor"]
    vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1

duplicate_vendor_names = [vendor for vendor, count in vendor_counts.items() if count > 1]

print(duplicate_vendor_names)

dict_counts = {}
for invoice in invoices:
    key = json.dumps(invoice, sort_keys=True)
    dict_counts[key] = dict_counts.get(key, 0) + 1

duplicate_full_invoices = [invoice for invoice in invoices if dict_counts[json.dumps(invoice, sort_keys=True)] > 1]

print(duplicate_full_invoices)
