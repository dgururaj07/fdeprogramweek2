import json
from fastapi import APIRouter,HTTPException
from homeassignments_w1day2Recap.invoicemodel import invoice
from homeassignments_w1day2Recap.getinvoices import JSON_FILE, load_invoices

router = APIRouter()

@router.put("/invoices/{invoice_id}", status_code=200)
#this checks of if the uRL sent in the URL matches with the request
def update_invoice(invoice_id: int, updated_invoice: invoice):
    # updated_invoice is already parsed/validated from the request body by FastAPI
    if updated_invoice.invoice_id != invoice_id:
        raise HTTPException(
            status_code=400,
            detail="Invoice ID in URL must match invoice id in request body"
        )

    invoices = load_invoices()
    for index, existing_invoice in enumerate(invoices):
        if existing_invoice["invoice_id"] == invoice_id:
            invoices[index] = updated_invoice.model_dump()
            print(f"existing_invoice: {existing_invoice}")
            print(f"updated_invoice: {updated_invoice}")

            with open(JSON_FILE, "w", encoding="utf-8") as file:
                json.dump(invoices, file, indent=2)

            return {
                "message": "Invoice is updated",
                "invoice": updated_invoice,
            }

    raise HTTPException(status_code=404, detail="Invoice not found")