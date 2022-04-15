from models import Voucher
from models import Customer
from models import Account,Transaction,TypeTransaction
from lib.service.service import generate_account_number
def get_all_customers():
    return Customer.all_customers()

def customer_by_email(email):
    customer = Customer.query_by_email(email)
    if customer:
        return customer
    return None
def customer_store( lastname, firstname, phone, password,email,id_admin):
    if not Customer.query_by_email(email):
        print ('email is not exist')
        customer = Customer.Customer(firstname=firstname, lastname=lastname, email=email, phone=phone, password=password,admin_id=id_admin)
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


def customer_update(id, lastname, firstname, phone,email):
    customer = Customer.query_by_id(id)
    if customer:
        customer.lastname = lastname
        customer.firstname = firstname
        customer.phone = phone
        customer.email = email
        Customer.update_customer(customer)
        return True
    return False

def customer_by_id(id):
    customer = Customer.query_by_id(id)
    if customer:
        return customer
    return None


def customer_status_update(id):
    customer = Customer.query_by_id(id)
    if customer:
        if customer.status == 'active':
            customer.status = 'blocked'
        else:
            customer.status = 'active'
        Customer.status_update(customer)
        return True
    return False


def customer_by_account_number(account_number):
    account = Account.get_account(account_number)
    if account:
        return account.customer
    return None


def update_secret_code(id,code,newCode):
    customer = Customer.query_by_id(id)
    if customer:
        if customer.accounts.secret == code:
            customer.accounts.secret = newCode
            Customer.update_customer(customer)
            return customer
    return False

def deposit(id,amount):
    customer = Customer.query_by_id(id)
    if customer:
        voucher = Voucher.voucher_by_code(amount)
        if voucher:
            if voucher.status == 'active':
                if not voucher.is_used:
                    print("voucher is active")  
                    voucherAmount = voucher.amount  
                    customer.accounts.balance += voucherAmount
                    transaction=Transaction.Transaction(
                    account_id=customer.accounts.id,
                    amount=voucherAmount,
                    type_transaction_id=1,
                    status='success')
                    Transaction.add_transaction(transaction)
                    Customer.update_customer(customer)
                    Voucher.update_voucher(voucher)
                    return True
                else:
                    print("voucher is used")
                    return False
            else:
                print("voucher is not active")
                return False
        else:
            print("voucher is not exist")
            return False
    return False


def get_all_transactions(id):
    customer = Customer.query_by_id(id)
    if customer:
        return Transaction.get_transactions(customer.accounts.id)
    return None


def send(beneficiary, amount,id):
    customer = Customer.query_by_id(id)
    if customer:
        customer.accounts.balance -= amount
        transaction=Transaction.Transaction(
        account_id=customer.accounts.id,
        amount=amount,
        type_transaction_id=2,
        status='success')
        Transaction.add_transaction(transaction)
        Customer.update_customer(customer)
        transaction=Transaction.Transaction(
        account_id=beneficiary.accounts.id,
        amount=amount,
        type_transaction_id=1,
        status='success')
        Transaction.add_transaction(transaction)
        beneficiary.accounts.balance += amount
        Customer.update_customer(beneficiary)
        return True
    return False
