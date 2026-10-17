from fastapi import APIRouter, HTTPException
from homeassignments_w1day2Recap.invoicemodel import invoice
from homeassignments_w1day2Recap.getinvoices import JSON_FILE, load_invoices
import json

router = APIRouter()

@router.post("/invoices", status_code=201)
def create_invoice(new_invoice: invoice):
    invoices = load_invoices()

    for existing in invoices:
        if existing["invoice_id"] == new_invoice.invoiceid:
            raise HTTPException(status_code=409, detail="Invoice already exists")

    invoices.append(new_invoice.model_dump())

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(invoices, file, indent=2)

    return new_invoice
