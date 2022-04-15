from models import  Admin
from models import TypeTransaction
def get_all_admins():
    return Admin.all_admins()

def admin_store(username, password, email):
    if not Admin.query_by_email(email):
        print ('email is not exist')
        admin = Admin.Admin(username=username, email=email, password=password)
    
        Admin.add_admin(admin)
        return True

    return False


def get_admin_by_id(id):
    return Admin.get_admin_by_id(id)

def get_admin_by_email(email):
    return Admin.query_by_email(email)
    
def admin_remove(id):
    admin = Admin.get_admin_by_id(id)
    if admin:
        Admin.remove_admin(admin)
        return True
    return False


def admin_update(id, username, email):
    admin = Admin.get_admin_by_id(id)
    if admin:
        Admin.update_admin(admin, username, email)
        return True
    return False

