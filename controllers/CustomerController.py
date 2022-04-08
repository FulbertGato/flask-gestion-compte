from models import Customer
from models import Account

def get_all_customers():
    return Customer.all_customers()


def customer_store( lastname, firstname, phone, password,email):
    if not Customer.query_by_email(email):
        print ('email is not exist')
        customer = Customer.Customer(firstname=firstname, lastname=lastname, email=email, phone=phone, password=password)
        Customer.add_customer(customer)
        return True
    return False


