from fastapi import FastAPI,HTTPException
from .models import Invoice
from .services import get_invoice_by_id, create_invoice, update_invoice, delete_invoice

app = FastAPI()

@app.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: int):
    try:
        return get_invoice_by_id(invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@app.post("/invoices", response_model=Invoice)
def create_new_invoice(invoice: Invoice):
    return create_invoice(invoice.dict())   



@app.put("/invoices/{invoice_id}", response_model=Invoice)
def update_existing_invoice(invoice_id: int, updated_invoice: Invoice):
    try:
        return update_invoice(invoice_id, updated_invoice.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/invoices/{invoice_id}")
def delete_existing_invoice(invoice_id: int):
    try:
        delete_invoice(invoice_id)
        return {"message": f"Invoice with ID {invoice_id} deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    


