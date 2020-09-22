
class Session:

    @staticmethod
    def clean_payment_session(request) -> None:
        request.session['delayed_invoices'] = {}
        request.session['delayed_invoices']['total_dept'] = 0

    @staticmethod
    def remove_customer(request, customer):
        request.session['delayed_invoices'].pop(customer)
        request.session.modified = True
