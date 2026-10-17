from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float | None= None
    status: str
    date: str
