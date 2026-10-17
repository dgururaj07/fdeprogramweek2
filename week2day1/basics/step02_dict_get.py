invoices ={
    "invoice_id": 103,
    "vendor": "123 Industries",
    "amount": 95000,
    "status": "PENDING"
  }
#print(invoices["Address"])
print(invoices.get("Address","unknown"))