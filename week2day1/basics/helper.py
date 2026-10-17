def determine_approval(invoice_amount):
    if invoice_amount > 1000:
        return "Manager Approval Required "
    elif invoice_amount > 500:
        return "supperssor Approval Required"
    else:
        return "Standard Approval Required"