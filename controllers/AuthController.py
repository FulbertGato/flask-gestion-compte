
from models import Customer, Admin, Account


def login_admin(usersname, password):
    admin = Admin.query_by_email(usersname)
    if admin:
        if Admin.password_is_correct(admin.password, password):
            return admin
    if len(Admin.all_admins()) == 0:
        print('No admin')
        admin = Admin.Admin(username="admin", email="admin@gmail.com", password="1234")
        Admin.add_admin(admin)
    return False


def login_customer(phone, password):
    customer = Account.get_acount_by_customer_phone_and_secret(phone, password).customer
    if customer:
        return customer
    return False
    
    
