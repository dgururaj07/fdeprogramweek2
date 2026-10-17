from fastapi import APIRouter, HTTPException, Response, status

from models.invoices import Invoice
from services.invoiceService import (
    create_invoice,
    delete_invoice_by_id,
    read_all_invoices,
    read_invoice_by_id,
    update_invoice_by_id,
)

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=list[Invoice])
def get_invoices():
    return read_all_invoices()


@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str):
    invoice = read_invoice_by_id(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
def create_new_invoice(invoice: Invoice):
    return create_invoice(invoice.dict())


@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: str, invoice: Invoice):
    if invoice.invoice_id != invoice_id:
        raise HTTPException(
            status_code=400,
            detail="Path invoice_id must match body invoice_id",
        )

    updated = update_invoice_by_id(invoice_id, invoice.dict())
    if updated is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: str):
    if not delete_invoice_by_id(invoice_id):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)