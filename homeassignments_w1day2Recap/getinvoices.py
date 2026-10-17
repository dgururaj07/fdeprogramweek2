from fastapi import APIRouter
from pathlib import Path
import json


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "data" / "invoices.json"


def load_invoices():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

@router.get("/invoices")
def get_invoices():
    return load_invoices()

@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    invoices = load_invoices()
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return {"error": "Invoice not found"}   
