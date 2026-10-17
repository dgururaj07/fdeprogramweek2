from fastapi import APIRouter, HTTPException
import json
from homeassignments_w1day2Recap.getinvoices import JSON_FILE,load_invoices
router = APIRouter()

@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id:int):
    invoices = load_invoices()

    for index,invoice in enumerate(invoices):
        if invoice["invoice_id"] ==invoice_id:
            deleted_invoice=invoices.pop(index)
            with open(JSON_FILE, "w", encoding="utf-8") as file:
                json.dump(invoices, file, indent=2)

            return {
                "message": "Invoice is deleted",
                "invoice": deleted_invoice,
            }

    raise HTTPException(status_code=404, detail="Invoice not found")
