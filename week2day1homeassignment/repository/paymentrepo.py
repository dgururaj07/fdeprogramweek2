import json

DATA_PAYMENT_FILE = "data/payment.json"


# Reads the payments JSON file and returns its contents as a list of dicts.
def get_payments():
	with open(DATA_PAYMENT_FILE, "r") as file:
		return json.load(file)


# Saves the given list of payments, replacing the previous contents.
def save_payments(payments):
	with open(DATA_PAYMENT_FILE, "w") as file:
		json.dump(payments, file, indent=4)


# Appends a new payment to the file.
def create_payment(payment):
	payments = get_payments()
	if any(existing["payment_id"] == payment["payment_id"] for existing in payments):
		raise ValueError(f"Payment ID {payment['payment_id']} already exists")
	payments.append(payment)
	save_payments(payments)
	return payment


# Replaces the payment matching payment_id with updated_payment.
def update_payment(payment_id, updated_payment):
	payments = get_payments()
	for index, payment in enumerate(payments):
		if payment["payment_id"] == payment_id:
			if any(
				other_index != index
				and other_payment["payment_id"] == updated_payment["payment_id"]
				for other_index, other_payment in enumerate(payments)
			):
				raise ValueError(
					f"Payment ID {updated_payment['payment_id']} already exists"
				)
			payments[index] = updated_payment
			save_payments(payments)
			return updated_payment
	return None


# Removes the payment matching payment_id from the file.
def delete_payment(payment_id):
	payments = get_payments()
	for index, payment in enumerate(payments):
		if payment["payment_id"] == payment_id:
			del payments[index]
			save_payments(payments)
			return True
	return False
