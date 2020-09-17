
class Payments:
    invoice_list = []

    def __init__(self, customer, invoice_no, inv_create_date, inv_payment_term, total_gross_amount, current_gross_amount):
        self.customer = customer
        self.invoice_no = invoice_no
        self.inv_create_date = inv_create_date
        self.inv_payment_term = inv_payment_term
        self.total_gross_amount = total_gross_amount
        self.current_gross_amount = current_gross_amount
        Payments.invoice_list.append(self)

    @staticmethod
    def extract_payment_data(payment_data: str):
        """extracts payments data from 'Symfonia handel' report"""
        for line in payment_data.split('\n'):
            if len(line) > 5:
                customer, _, invoice_no, _, inv_create_date, inv_payment_term, _,_, total_gross_amount, current_gross_amount = line.split('\t')

