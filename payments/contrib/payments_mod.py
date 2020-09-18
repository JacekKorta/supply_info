
class Invoice:
    invoice_list = []

    def __init__(self, customer, invoice_no, inv_create_date, inv_payment_term, total_gross_amount, current_gross_amount):
        self.customer = customer
        self.invoice_no = invoice_no
        self.inv_create_date = inv_create_date
        self.inv_payment_term = inv_payment_term
        self.total_gross_amount = total_gross_amount
        self.current_gross_amount = current_gross_amount
        Invoice.invoice_list.append(self)

    @staticmethod
    def extract_payment_data(payment_data: str) -> None:
        """extracts payments data from 'Symfonia handel' report"""
        for line in payment_data.split('\n'):
            if len(line) > 5:
                customer, _, invoice_no, _, inv_create_date, inv_payment_term,\
                    _, _, total_gross_amount, current_gross_amount = line.split('\t')

                Invoice(customer, invoice_no, inv_create_date,
                         inv_payment_term, total_gross_amount, current_gross_amount)

    @staticmethod
    def get_customer_list() -> list:
        customers = []
        for item in Invoice.invoice_list:
            if item.customer not in customers:
                customers.append(item.customer)
        return customers

    @staticmethod
    def get_customer_total_dept(customer: str) -> float:
        total_dept = 0
        for item in Invoice.invoice_list:
            if item.customer == customer:
                total_dept += float(item.total_gross_amount)
        return round(total_dept, 2)

