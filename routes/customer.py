from flask import Blueprint, flash, redirect, render_template, request, session
from app import app
from lib.validator.granted_validor import is_connected,  is_customer
from controllers import CustomerController
customer_bp = Blueprint('customer_bp', __name__)


@app.route('/customer', methods=['GET'])
def customer():
    if  is_connected():
        if is_customer():
            id = session['user_connect']['email']
            customer = CustomerController.customer_by_email(id)
            return render_template("client/dashboard.html", customer=customer)
            
    return redirect('/')


@app.route('/customer/profile', methods=['GET'])
def customer_profile():
    if  is_connected():
        if is_customer():
            id = session['user_connect']['email']
            customer = CustomerController.customer_by_email(id)
            return render_template("client/profil.html", customer=customer)
            
    return redirect('/')

#change secret code
@app.route('/customer/code/update', methods=['POST'])
def customer_change_secret_post():
    if  is_connected():
        if is_customer():
            if request.form['id']  and request.form['code'] and request.form['newCode'] and request.form['codeConfirme'] :
                id = request.form['id']
                code = request.form['code']
                newCode = request.form['newCode']
                codeConfirme = request.form['codeConfirme']
                if newCode == codeConfirme:
                    customer = CustomerController.update_secret_code(id, code, newCode)
                    if customer:
                        session['user_connect']= customer.serialize()
                        flash('Votre code a été modifié avec succès')
                    else:
                        flash('Le code secret est incorrect')               
                return redirect('/customer/profile')           
    return redirect('/')

# deposit
@app.route('/customer/deposit', methods=['GET'])
def customer_deposit():
    if  is_connected():
        if is_customer():
            return render_template("client/deposit.html")           
    return redirect('/')


@app.route('/customer/deposit/post', methods=['POST'])
def customer_deposit_post():
    if  is_connected():
        if is_customer():
            if request.form['id']  and request.form['amount'] :  
                id = session['user_connect']['email']
                customerGet = CustomerController.customer_by_email(id)            
                id = customerGet.id
                amount = request.form['amount']
                customer = CustomerController.deposit(id=id, amount=amount)                   
                if customer:
                    
                    flash('Votre compte a été crédité avec succès')
                     
                else:
                    flash("Vous pouvez pas utilisez ce code")
            return redirect('/customer/deposit')            
    return redirect('/')


# liste des transactions
@app.route('/customer/transactions', methods=['GET'])
def customer_transactions():
    if  is_connected():
        if is_customer():
            transactions=CustomerController.get_all_transactions(session['user_connect']['id'])
            return render_template("client/transactions.html", transactions=transactions)           
    return redirect('/')

# send money
@app.route('/customer/send', methods=['GET'])
def customer_send():
    if  is_connected():
        if is_customer():
            return render_template("client/send.html")           
    return redirect('/')


@app.route('/customer/send/post', methods=['POST'])
def customer_send_post():
    if  is_connected():
        if is_customer():
            if  request.form['amount'] and request.form['account_number'] :              
                id = session['user_connect']['email']
                customerGet = CustomerController.customer_by_email(id)            
                id = customerGet.id
                amount = float(request.form['amount'])
                account_number = request.form['account_number']
                if amount >= 500 and amount < 5000:
                    if customerGet.accounts.account_number != account_number:
                        if customerGet.accounts.balance >= amount and customerGet.accounts.balance - amount >= 1000:
                            beneficiary = CustomerController.customer_by_account_number(account_number)
                            if beneficiary:
                                if beneficiary.status == 'active':
                                    statut = CustomerController.send(beneficiary=beneficiary, amount=amount,id=id)
                                    if statut:
                                        session['user_connect']= CustomerController.customer_by_id(id).serialize()
                                        flash('Votre transaction a été effectuée avec succès')
                                        return redirect('/customer/transactions')
                                    else:
                                        flash('Votre transaction a été refusée')
                                        return redirect('/customer/send')
                                flash('Le compte bénéficiaire est inactif')
                                return redirect('/customer/send')
                            flash('Le compte bénéficiaire n\'existe pas')
                            return redirect('/customer/send')
                        flash('Le montant est insuffisant')
                        return redirect('/customer/send')
                    flash('Le compte bénéficiaire est incorrect')
                    return redirect('/customer/send')
                flash('Le montant est incorrect (500 - 5000 FCFA)')
                return redirect('/customer/send')         
    return redirect('/')