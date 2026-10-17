# Week 2 Day 1 Invoice and Payment API

A small FastAPI application that provides CRUD endpoints for invoices and payments. Records are stored in JSON files under `data/`.

## Requirements

- Python 3.10 or newer
- Dependencies listed in `../requirement.txt`

## Setup and Run

From the repository root, enter this project directory and install the dependencies:

```powershell
cd .\week2day1homeassignment
python -m pip install -r ..\requirement.txt
```

Start the development server from `week2day1homeassignment` so the relative data-file paths resolve correctly:

```powershell
python -m uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

## Endpoints

### Invoices

| Method | Endpoint | Purpose | Success status |
|---|---|---|---:|
| GET | `/invoices/` | Retrieve all invoices | 200 |
| GET | `/invoices/{invoice_id}` | Retrieve one invoice | 200 |
| POST | `/invoices/` | Create an invoice | 201 |
| PUT | `/invoices/{invoice_id}` | Replace an invoice | 200 |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice | 204 |

Invoice request body:

```json
{
  "invoice_id": "INV-108",
  "vendor": "Acme Supplies",
  "amount": 2450.75,
  "status": "PENDING",
  "date": "2026-10-17"
}
```

`amount` may be `null`.

### Payments

| Method | Endpoint | Purpose | Success status |
|---|---|---|---:|
| GET | `/payments` | Retrieve all payments | 200 |
| GET | `/payments/{payment_id}` | Retrieve one payment | 200 |
| POST | `/payments` | Create a payment | 201 |
| PUT | `/payments/{payment_id}` | Replace a payment | 200 |
| DELETE | `/payments/{payment_id}` | Delete a payment | 204 |

Payment request body:

```json
{
  "payment_id": "PAY-005",
  "invoice_id": "INV-108",
  "paid": 2450.75
}
```

Payment IDs must be unique. `paid` must be a non-negative number.

## Error Responses

- `400 Bad Request`: the ID in an update path does not match the ID in the request body.
- `404 Not Found`: the requested invoice or payment does not exist.
- `409 Conflict`: a payment ID is already in use.
- `422 Unprocessable Entity`: a request body does not satisfy its model schema.

## Data Files

- Invoices: `data/invoices.json`
- Payments: `data/payment.json`

Successful create, update, and delete requests write changes to these files.

## Invoice Processing Script

`dataUtils/invoice_processing.py` runs a separate invoice-cleanup and payment-reconciliation exercise using sample data defined in the script. Run it from the `week2day1homeassignment` directory:

```powershell
python .\dataUtils\invoice_processing.py
```

The script prints the results of these steps:

1. **Normalize invoice data:** trim and title-case vendor names, uppercase statuses, and report invoices with missing amounts.
2. **Remove exact duplicates:** identify identical invoice records and keep the first occurrence.
3. **Find suspected duplicates:** report records with the same vendor, amount, and date but different invoice IDs; records with missing amounts are skipped.
4. **Process credit notes:** match negative invoices with positive invoices for the same vendor and absolute amount, then mark both as `CANCELLED`.
5. **Reconcile payments:** total payments by invoice ID, report balances and payment statuses, and identify unmatched or ambiguous payments.

This script operates on in-memory sample lists and prints reports to the console. It does not read from or write to the API's JSON data files.

## Postman Collection

Import [`../postman/invoice-payment-api.postman_collection.json`](../postman/invoice-payment-api.postman_collection.json) into Postman for the invoice and payment CRUD requests. The collection uses `http://127.0.0.1:8000` as its default `baseUrl` and generates IDs for create requests.
