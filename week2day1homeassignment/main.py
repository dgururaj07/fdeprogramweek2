from fastapi import FastAPI

from routers.invoiceRouter import router as invoice_router
from routers.paymentRouter import router as payment_router


app = FastAPI()
app.include_router(invoice_router)
app.include_router(payment_router)
