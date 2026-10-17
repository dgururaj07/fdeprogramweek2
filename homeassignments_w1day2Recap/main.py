from fastapi import FastAPI
import importlib

get_invoices = importlib.import_module("homeassignments_w1day2Recap.getinvoices").router
create_invoices = importlib.import_module("homeassignments_w1day2Recap.create_inv").router
delete_invoices = importlib.import_module("homeassignments_w1day2Recap.deleteinvoice").router
update_invoices = importlib.import_module("homeassignments_w1day2Recap.updateinv").router


app=FastAPI()
app.include_router(get_invoices)
app.include_router(create_invoices)
app.include_router(delete_invoices)
app.include_router(update_invoices)