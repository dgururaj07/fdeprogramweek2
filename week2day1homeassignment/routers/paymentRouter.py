from fastapi import APIRouter, HTTPException, Response, status

from models.payment import Payment
from services.paymentService import (
	DuplicatePaymentIdError,
	create_payment,
	delete_payment_by_id,
	read_all_payments,
	read_payment_by_id,
	update_payment_by_id,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("", response_model=list[Payment], status_code=status.HTTP_200_OK)
def get_payments():
	return read_all_payments()


@router.get("/{payment_id}", response_model=Payment, status_code=status.HTTP_200_OK)
def get_payment(payment_id: str):
	payment = read_payment_by_id(payment_id)
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")
	return payment


@router.post("", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_new_payment(payment: Payment):
	try:
		return create_payment(payment.model_dump())
	except DuplicatePaymentIdError as error:
		raise HTTPException(status_code=409, detail=str(error)) from error


@router.put("/{payment_id}", response_model=Payment, status_code=status.HTTP_200_OK)
def update_existing_payment(payment_id: str, payment: Payment):
	if payment.payment_id != payment_id:
		raise HTTPException(
			status_code=400,
			detail="Path payment_id must match body payment_id",
		)

	try:
		updated = update_payment_by_id(payment_id, payment.model_dump())
	except DuplicatePaymentIdError as error:
		raise HTTPException(status_code=409, detail=str(error)) from error

	if updated is None:
		raise HTTPException(status_code=404, detail="Payment not found")
	return updated


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_payment(payment_id: str):
	if not delete_payment_by_id(payment_id):
		raise HTTPException(status_code=404, detail="Payment not found")
	return Response(status_code=status.HTTP_204_NO_CONTENT)
