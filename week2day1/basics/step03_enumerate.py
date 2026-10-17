invoices = [
  {
    "invoice_id": 103,
    "vendor": "123 Industries",
    "amount": 95000,
    "status": "PENDING"
  },
  {
    "invoice_id": 104,
    "vendor": "RAJ CORPORATION",
    "amount": 8000,
    "status": "PENDING"
  },
  {
    "invoice_id": 105,
    "vendor": "LIC CORPORATION",
    "amount": 6000,
    "status": "PAID"
  },
  {
    "invoice_id": 106,
    "vendor": "DGR",
    "amount": 10000,
    "status": "unpaid"
  }
]


for index,invoice in enumerate(invoices):
    if invoice["invoice_id"] == 105:
        invoices[index]["invoice_id"] = 197

    
    print(index,invoice)    

    
