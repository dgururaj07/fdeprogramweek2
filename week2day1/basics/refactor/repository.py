import json
DATA_FILE = "week2day1/data/invoices.json"

# Reads the invoices JSON file and returns its contents as a Python list/dict
def load_invoices():
    with open(DATA_FILE,"r", encoding="utf-8") as f:
        return json.load(f)


# Writes the given invoices back to the JSON file, overwriting its previous contents
def save_invoices(invoices):
    with open(DATA_FILE,"w", encoding="utf-8") as f:
        json.dump(invoices,f,indent=4)


def get_invoice_by_id(invoice_id):
    invoices = load_invoices()
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


def add_invoice(invoice):
    invoices = load_invoices()
    invoices.append(invoice)
    save_invoices(invoices)

def update_invoice(invoice_id, updated_invoice):
    invoices = load_invoices()
    for i, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            invoices[i] = updated_invoice
            save_invoices(invoices)
            return True
    return False


def delete_invoice(invoice_id):
    invoices = load_invoices()
    for index, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            del invoices[index]
            save_invoices(invoices)
            return True
