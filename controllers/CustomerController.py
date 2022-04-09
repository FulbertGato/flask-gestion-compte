from models import Customer
from models import Account
from lib.service.service import generate_account_number
def get_all_customers():
    return Customer.all_customers()


def customer_store( lastname, firstname, phone, password,email):
    if not Customer.query_by_email(email):
        print ('email is not exist')
        customer = Customer.Customer(firstname=firstname, lastname=lastname, email=email, phone=phone, password=password)
        Customer.add_customer(customer)
        customer=Customer.query_by_email(email)
       
        account=Account.Account(account_number=generate_account_number(),customer_id=customer.id,balance=0,secret='0000')
        Account.add_account(account)
        return True
    return False


def customer_remove(id):
    customer = Customer.query_by_id(id)
    if customer:
        Customer.remove_customer(customer)
        return True
    return False


