from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_id: int
    amount: float
    status: str
    vendor: str = "UNKNOWN"