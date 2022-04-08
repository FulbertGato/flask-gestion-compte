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
    #get attributes from request
    
    if role == 'admin' or role == 'customer':
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
            if request.form['email']  and request.form['password'] :
                username = request.form['email'] 
                password = request.form['password']
                customer = AuthController.login_customer(username, password)
                if customer:
                    return redirect('/customer')
            flash('Les données saisies sont incorrectes')
            return redirect('/login/customer')
    return redirect('/')
    
@app.route('/', methods=['GET'])
def visiteur():
    if  is_connected():
        if is_admin():
            return redirect('/admin')
        elif is_customer():
            return redirect('/customer')
    return render_template("auth/visiteur.html")