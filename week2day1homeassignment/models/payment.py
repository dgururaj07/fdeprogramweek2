
from pydantic import BaseModel, Field, ConfigDict


class Payment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_id: str = Field(min_length=1)
    invoice_id: str = Field(min_length=1)
    paid: float = Field(ge=0, allow_inf_nan=False)
