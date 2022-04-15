from flask import Blueprint, flash, redirect, render_template, request
from flask import session
from app import app
from lib.validator.granted_validor import is_connected,  is_distributeur
from controllers import DistributeurController,CustomerController
distributeur_bp = Blueprint('distributeur_bp', __name__)


@app.route('/distributeur', methods=['GET'])
def distributeur():
    if is_connected():
        if is_distributeur():
            return render_template('distributeur/dashboard.html')
    return redirect('/')


@app.route('/distributeur/profile', methods=['GET'])
def profil():
    if is_connected():
        if is_distributeur():
            return render_template('distributeur/profil.html')
    return redirect('/')


#edit password
@app.route('/distributeur/edit_password', methods=['GET', 'POST'])
def edit_password():
    if is_connected():
        if is_distributeur():
            if request.method == 'POST':
                old_password = request.form['old_password']
                new_password = request.form['new_password']
                confirm_password = request.form['confirm_password']
                if old_password and new_password and confirm_password:
                    if new_password == confirm_password:
                        id = session['user_connect']['id']
                        if DistributeurController.edit_password(id,old_password, new_password):
                            flash('Mot de passe modifié avec succès', 'success')
                        else:
                            flash('Mot de passe incorrect', 'danger')
                    else:
                        flash('Les mots de passe ne sont pas identiques', 'danger')
                else:
                    flash('Veuillez remplir tous les champs', 'danger')
            return render_template('distributeur/profil.html')
    return redirect('/')


#depot de fonds sur compte courant
@app.route('/distributeur/depot', methods=['GET', 'POST'])
def depot():
    if is_connected():
        if is_distributeur():
            if request.method == 'POST':
                amount = request.form['amount']
                account_number = request.form['account_number']
                if amount and amount.isdigit() and int(amount) > 1000 and int(amount) < 50000:
                    if account_number :
                        id = session['user_connect']['id']
                        beneficiary = CustomerController.customer_by_account_number(account_number)
                        if beneficiary:
                            if beneficiary.status == 'active':
                                flash('Vous avez déposé '+amount+' FCFA sur le compte '+account_number, 'success')
                                return DistributeurController.depositFunds(distributeur_id = id,beneficiary=beneficiary, amount=amount)
                            flash('Le compte bénéficiaire est inactif', 'danger')
                    flash('Veuillez saisir un numero de compte correct', 'danger')
                else:
                    flash('Veuillez entrer un montant valide', 'danger')
            return render_template('distributeur/depot.html')
    return redirect('/')


#voir les vouchers
@app.route('/distributeur/vouchers', methods=['GET'])
def vouchers():
    if is_connected():
        if is_distributeur():
            email = session['user_connect']['email']
            
            vouchers = DistributeurController.get_vouchers(email)
           
            return render_template('distributeur/vouchers.html', vouchers=vouchers)
    return redirect('/')


#update voucher
@app.route('/distributeur/voucher/status/update/<int:id>', methods=['GET'])
def update_voucher(id):
    if is_connected():
        if is_distributeur():
            if DistributeurController.update_voucher_status(id):
                flash('Voucher mis à jour avec succès', 'success')
            else:
                flash('Vous pouvez pas annuler le code ', 'danger')
    return redirect('/distributeur/vouchers')