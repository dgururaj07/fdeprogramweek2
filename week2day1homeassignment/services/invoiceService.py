from models.invoices import Invoice
from repository import invoicerepo


 # Return every invoice stored in the repository.
def read_all_invoices():
	return invoicerepo.get_invoices()


# Replace the stored invoice list with the supplied list.
def write_all_invoices(invoices):
	invoicerepo.save_invoices(invoices)
	return invoices


# Save one invoice through the repository.
def create_invoice(invoice):
	return invoicerepo.create_invoice(invoice)


# Return the invoice with this ID, or None when it is not found.
def read_invoice_by_id(invoice_id):
	for invoice in read_all_invoices():
		if invoice["invoice_id"] == invoice_id:
			return invoice
	return None


# Replace the invoice matching this ID; return None if it is not found.
def update_invoice_by_id(invoice_id, updated_invoice):
	return invoicerepo.update_invoice(invoice_id, updated_invoice)


# Delete the invoice matching this ID; return False if it is not found.
def delete_invoice_by_id(invoice_id):
	return invoicerepo.delete_invoice(invoice_id)
