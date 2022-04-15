import random
import string
from models import  Distributeur,Voucher


def get_all_distributeurs():
    return Distributeur.all_distributeurs()


def distributeur_store(nom,prenom,email,password):
    if not Distributeur.query_by_email(email):
        print ('email is not exist')
        distributeur = Distributeur.Distributeur(nom=nom, prenom=prenom, email=email, password=password)
        print (distributeur)
        Distributeur.add_distributeur(distributeur)
        return True
    return False


def distributeur_by_id(id):
    return Distributeur.query_by_id(id)


def distributeur_remove(id):
    return Distributeur.delete_distributeur(id)


def distributeur_update(id, nom, prenom, email):
    distributeur = Distributeur.query_by_id(id)
    if distributeur:
        Distributeur.update_distributeur(id, nom=nom, prenom=prenom, email=email)
        return True
    return False

def distributeur_status_update(id):
    distributeur = Distributeur.query_by_id(id)
    if distributeur:
        if distributeur.status == 'active':
            Distributeur.update_distributeur_status(id, status='inactive')
        else:
            Distributeur.update_distributeur_status(id, status='active')
        return True
    return False

def edit_password(id, old_password, new_password):
    distributeur = Distributeur.query_by_id(id)
    if distributeur:
        if Distributeur.password_is_correct(distributeur.password, old_password):
            Distributeur.update_distributeur_password(id, password=new_password)
            return True
        return False

def generate_voucher_code(account_number):
    return account_number+''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + account_number

def depositFunds(beneficiary, distributeur_id,amount):
    distributeur = Distributeur.query_by_id(distributeur_id)
    if distributeur:
            
            voucherCode = generate_voucher_code(beneficiary.accounts.account_number)
           
            voucher = Voucher.Voucher(
                code=voucherCode,
                account_id=beneficiary.accounts.id,
                distributeur_id=distributeur.id,
                amount=amount)
            Voucher.add_voucher(voucher)
            return voucher.code
    return "haha"


def get_vouchers(email):
    distributeur = Distributeur.query_by_email(email)
    if distributeur:
      
        return distributeur.vouchers
    return []

def update_voucher_status(id):
    voucher = Voucher.query_by_id(id)
    if voucher:
        if voucher.status == 'active' and voucher.is_used == False:
           return Voucher.update_voucher_status(id, status='inactive')
        
    return False
            

