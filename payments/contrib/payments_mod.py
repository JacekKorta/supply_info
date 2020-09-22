from datetime import datetime


class Invoice:
    invoices_list = []
    delayed_invoices_list = []

    def __init__(self, customer, invoice_no, inv_create_date, inv_payment_term, total_gross_amount, current_gross_amount):
        self.customer = customer
        self.invoice_no = invoice_no
        self.inv_create_date = inv_create_date
        self.inv_payment_term = inv_payment_term
        self.total_gross_amount = total_gross_amount
        self.current_gross_amount = current_gross_amount
        Invoice.invoices_list.append(self)

    @staticmethod
    def extract_payment_data(payment_data: str) -> None:
        """extracts payments data from 'Symfonia handel' report."""
        for line in payment_data.split('\n'):
            if len(line.split('\t')) > 5:
                customer, _, invoice_no, _, inv_create_date, inv_payment_term,\
                    _, _, total_gross_amount, current_gross_amount, *_ = line.split('\t')
                if invoice_no != 'dokument':
                    try:
                        Invoice(customer,
                                invoice_no,
                                datetime.strptime(inv_create_date, '%Y-%m-%d'),
                                datetime.strptime(inv_payment_term, '%Y-%m-%d'),
                                total_gross_amount,
                                current_gross_amount)
                    except ValueError:
                        continue

    @staticmethod
    def get_customer_list(invoices: list) -> list:
        customers = []
        for item in invoices:
            if item.customer not in customers:
                customers.append(item.customer)
        return customers

    @staticmethod
    def get_delayed_invoices() -> None:
        today = datetime.today()
        for invoice in Invoice.invoices_list:
            if invoice.inv_payment_term < today: # zmień jeśli ma pokazywać faktury przeterminowane dzisiaj
                Invoice.delayed_invoices_list.append(invoice)

    @staticmethod
    def get_customer_total_dept(customer: str, invoices: list) -> float:
        total_dept = 0
        for item in invoices:
            if item.customer == customer:
                total_dept += float(item.total_gross_amount.replace(',', '.'))
        return round(total_dept, 2)

    @staticmethod
    def invoices_to_dict() -> dict:
        delayed_invoices_dict = {}
        for item in Invoice.delayed_invoices_list:
            if item.customer not in delayed_invoices_dict.keys():
                delayed_invoices_dict[item.customer] = {'invoices': {}}
            delayed_invoices_dict[item.customer]['invoices'][item.invoice_no] = \
                {'inv_create_date': datetime.strftime(item.inv_create_date, '%Y-%m-%d'),
                 'inv_payment_term': datetime.strftime(item.inv_payment_term, '%Y-%m-%d'),
                 'total_gross_amount': item.total_gross_amount,
                 'current_gross_amount': item.current_gross_amount}
        for customer in delayed_invoices_dict.keys():
            total_dept = Invoice.get_customer_total_dept(customer, Invoice.delayed_invoices_list)
            delayed_invoices_dict[customer]['total_dept'] = total_dept
        return delayed_invoices_dict
