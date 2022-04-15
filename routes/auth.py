from flask import Blueprint, session,flash,jsonify, url_for
from flask import render_template, request, make_response, redirect
from controllers import AuthController
from app import app
from lib.validator.granted_validor import is_connected, is_admin, is_customer
auth_bp = Blueprint('auth_bp', __name__)
@app.route('/login/<string:role>', methods=['GET'])
def login(role):
    
    if  is_connected():
        return redirect('/')
    if role == 'admin' or role == 'customer' or role == 'distributeur':
        if request.args.get('username'):
            username = request.args.get('username')
            return render_template("auth/login.html", role=role,username=username)
        else:
            return render_template("auth/login.html", role=role)
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login_post():
    if  is_connected():
       return redirect('/')
    if request.method == 'POST':
        if request.form['role'] == 'admin':
            if request.form['email']  and request.form['password']  :
                username = request.form['email'] 
                password = request.form['password']
                admin = AuthController.login_admin(username, password)
                if admin:
                    #creer une session
                    session['user_connect'] = admin.serialize()
                    #si le login est valide, rediriger vers la page d'admin
                    return redirect('/admin')
            flash('Les données saisies sont incorrectes')
            return redirect(url_for('login', role='admin', username=username))
                

        elif request.form['role'] == 'customer':
            if request.form['phone']  and request.form['password'] :
                phone= request.form['phone'] 
                secret = request.form['password']
                customer = AuthController.login_customer(phone, secret)
                if customer:
                    
                    if customer.status == 'active':
                        #creer une session
                        session['user_connect'] = customer.serialize()
                        return redirect('/customer')
                    else:
                        flash('Votre compte est désactivé')
                        return redirect(url_for('login', role='customer', phone=phone))
            flash('Les données saisies sont incorrectes')
            return redirect(url_for('login', role='customer', phone=phone))
        elif request.form['role'] == 'distributeur':
            if request.form['email']  and request.form['password']  :
                username = request.form['email'] 
                password = request.form['password']
                distributeur = AuthController.login_distributeur(username, password)
                if distributeur:
                    if distributeur.status == 'active':
                        #creer une session
                        session['user_connect'] = distributeur.serialize()
                        return redirect('/distributeur')
                    flash('Votre compte est désactivé')
                    return redirect(url_for('login', role='distributeur', username=username))
            flash('Les données saisies sont incorrectes')
            return redirect(url_for('login', role='distributeur', username=username))
    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    if  is_connected():
        session.clear()
        return redirect('/')
    return redirect('/')  



@app.route('/', methods=['GET'])
def visiteur():
    if  is_connected():
        if is_admin():
            return redirect('/admin')
        elif is_customer():
            return redirect('/customer')
    return render_template("auth/visiteur.html")