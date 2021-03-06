from tokenize import Number
from flask import Blueprint, redirect, render_template, request
from controllers import AdminController, CustomerController
from app import app
from lib.validator.granted_validor import is_connected, is_admin, is_customer
admin_bp = Blueprint('admin_bp', __name__)
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if  is_connected():
        if is_admin():
            return render_template("admin/dashboard.html")
    return redirect('/')

#list of admin
@app.route('/admin/list', methods=['GET'])
def admin_list():
    if  is_connected():
        if is_admin():
            admins=AdminController.get_all_admins()
            return render_template("admin/list.html", admins=admins)
    return redirect('/')

@app.route('/admin/add', methods=['GET'])
def admin_add():
    if  is_connected():
        if is_admin():
            return render_template("admin/add.html")
    return redirect('/')

@app.route('/admin/add', methods=['POST'])
def admin_add_post():
    if  is_connected():
        if is_admin():
            username=request.form['username']
            password="passer@123"
            email=request.form['email']
            if username and password and email:
                if AdminController.admin_store(username, password, email):
                    return redirect('/admin/list')
            return redirect('/admin/add')
    return redirect('/')


@app.route('/admin/remove/<int:id>', methods=['GET'])
def admin_remove(id):
    if  is_connected():
        if is_admin():
            if AdminController.admin_remove(id):
                return redirect('/admin/list')
    return redirect('/')


@app.route('/admin/update/<int:id>', methods=['GET'])
def admin_update(id):
    if  is_connected():
        if is_admin():
            admin=AdminController.get_admin_by_id(id)
            if admin:
                return render_template("admin/update.html", admin=admin)
    return redirect('/')


@app.route('/admin/update/<int:id>', methods=['POST'])
def admin_update_post(id):
    if  is_connected():
        if is_admin():
            username=request.form['username']
            email=request.form['email']
            if username and email:
                if AdminController.admin_update(id, username, email):
                    return redirect('/admin/list')
            return redirect('/admin/update/'+str(id))
    return redirect('/')


@app.route('/admin/customer/add', methods=['GET'])
def customer_add():
    if  is_connected():
        if is_admin():
            return render_template("client/add.html")
    return redirect('/')


@app.route('/admin/customer/add', methods=['POST'])
def customer_add_post():
    
    if  is_connected():
        if is_admin():            
            lastname=request.form['lastname']
            firstname=request.form['firstname']
            phone=request.form['phone']
            password="passer@123"
            email=request.form['email']
            
            if lastname and firstname and phone  and email:               
                if CustomerController.customer_store(lastname=lastname, firstname=firstname, phone=phone, password=password, email=email):
                   # return "je suis un bg"
                    return redirect('/admin/customer/list')
            return redirect('/admin/customer/add')
    return redirect('/')

@app.route('/admin/customer/list', methods=['GET'])
def customer_list():
    if  is_connected():
        if is_admin():
            customers=CustomerController.get_all_customers()
            return render_template("client/list.html", customers=customers)
    return redirect('/')


@app.route('/admin/customer/remove/<int:id>', methods=['GET'])
def customer_remove(id):
    if  is_connected():
        if is_admin():
            if CustomerController.customer_remove(id):
                return redirect('/admin/customer/list')
    return redirect('/')
    
@app.route('/admin/customer/view/<int:id>', methods=['GET'])
def customer_view(id):
    if  is_connected():
        if is_admin():
            customer=CustomerController.customer_by_id(id)
            return render_template("client/view.html", customer=customer)
    return redirect('/')

@app.route('/admin/customer/update', methods=['POST'])
def customer_update():
    if  is_connected():
       
        id=request.form['id']
        lastname=request.form['lastname']
        firstname=request.form['firstname']
        phone=request.form['phone']
        email=request.form['email']
        if lastname and firstname and phone and email:
            if CustomerController.customer_update(id, lastname=lastname, firstname=firstname, phone=phone, email=email):
                 if is_admin():
                    return redirect('/admin/customer/list')
                 else:
                    return redirect('/')
            return redirect('/admin/customer/view/'+str(id))
    return redirect('/')


@app.route('/admin/customer/update/status/<int:id>', methods=['GET'])
def customer_update_status(id):
    if  is_connected():
        if is_admin():
            if CustomerController.customer_status_update(id):
                return redirect('/admin/customer/list')
    return redirect('/')


@app.route('/admin/customer/search', methods=['GET'])
def customer_search():
    if  is_connected():
        if is_admin():
            return render_template("client/search.html")
    return redirect('/')


@app.route('/admin/customer/search', methods=['POST'])
def customer_search_post():
    if  is_connected():
        if is_admin():
            number=request.form['number']
            customer=CustomerController.customer_by_account_number(number)
            if customer:
                 return redirect('/admin/customer/view/'+str(customer.id))
            return redirect('/admin/customer/search')
    return redirect('/')