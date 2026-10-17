import json

DATA_INVOICE_FILE = "data/invoices.json"


# Reads the invoices JSON file and returns its contents as a list of dicts
def get_invoices():
    with open(DATA_INVOICE_FILE, "r") as f:
        return json.load(f)


# Saves the given list of invoices back to the JSON file, overwriting its previous contents
def save_invoices(invoices):
    with open(DATA_INVOICE_FILE, "w") as f:
        json.dump(invoices, f, indent=4)


# Appends a new invoice to the file
def create_invoice(invoice):
    invoices = get_invoices()
    invoices.append(invoice)
    save_invoices(invoices)
    return invoice


# Finds the invoice matching invoice_id and replaces it with updated_invoice
def update_invoice(invoice_id, updated_invoice):
    invoices = get_invoices()
    for index, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            invoices[index] = updated_invoice
            save_invoices(invoices)
            return updated_invoice
    return None


# Removes the invoice matching invoice_id from the file
def delete_invoice(invoice_id):
    invoices = get_invoices()
    for index, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            del invoices[index]
            save_invoices(invoices)
            return True
    return False
