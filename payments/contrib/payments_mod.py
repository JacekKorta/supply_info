
class Payments:
    invoice_list = []

    def __init__(self, customer, invoice_no, inf_create_date, inv_payment_term, total_gross_amount, current_gross_amount):
        self.customer = customer
        self.invoice_no = invoice_no
        self.inf_create_date = inf_create_date
        self.inv_payment_term = inv_payment_term
        self.total_gross_amount = total_gross_amount
        self.current_gross_amount = current_gross_amount
        Payments.invoice_list.append(self)


