from . import repository
from .models import Invoice

def get_invoice_by_id(invoice_id: int) -> Invoice:
    invoice_data = repository.get_invoice_by_id(invoice_id)
    if invoice_data is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    return Invoice(**invoice_data)

def create_invoice(invoice_data: dict) -> Invoice:
    new_invoice = Invoice(invoice_data)
    repository.add_invoice(new_invoice.dict())
    return new_invoice



def update_invoice(invoice_id: int, updated_data: dict) -> Invoice:
    existing_invoice = repository.get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    
    updated_invoice = Invoice(**existing_invoice, **updated_data)
    repository.update_invoice(invoice_id, updated_invoice.dict())
    return updated_invoice

def delete_invoice(invoice_id: int) -> None:
    existing_invoice = repository.get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    
    repository.delete_invoice(invoice_id)