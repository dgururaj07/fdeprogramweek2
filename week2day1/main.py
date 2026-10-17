import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
DATA_FILE = "data/invoices.json"

app = FastAPI()


class Invoice(BaseModel):
    invoice_id:str
    vendor:str
    amount:float
    status:str


