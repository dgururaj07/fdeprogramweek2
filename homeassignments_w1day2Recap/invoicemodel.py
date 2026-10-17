from pydantic import BaseModel

class invoice(BaseModel):
    invoice_id: int
    vendor: str
    amount: float
    status: str

