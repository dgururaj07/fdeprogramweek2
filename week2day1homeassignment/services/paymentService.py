from models.payment import Payment
from repository import paymentrepo


class DuplicatePaymentIdError(Exception):
	"""Raised when a payment ID is already assigned to another payment."""


# Return every payment stored in the repository.
def read_all_payments():
	return paymentrepo.get_payments()


# Replace the stored payment list with the supplied list.
def write_all_payments(payments):
	paymentrepo.save_payments(payments)
	return payments


# Save one payment through the repository.
def create_payment(payment):
	try:
		return paymentrepo.create_payment(payment)
	except ValueError as error:
		raise DuplicatePaymentIdError(str(error)) from error


# Return the payment with this ID, or None when it is not found.
def read_payment_by_id(payment_id):
	for payment in read_all_payments():
		if payment["payment_id"] == payment_id:
			return payment
	return None


# Replace the payment matching this ID; return None if it is not found.
def update_payment_by_id(payment_id, updated_payment):
	try:
		return paymentrepo.update_payment(payment_id, updated_payment)
	except ValueError as error:
		raise DuplicatePaymentIdError(str(error)) from error


# Delete the payment matching this ID; return False if it is not found.
def delete_payment_by_id(payment_id):
	return paymentrepo.delete_payment(payment_id)
