from flask import session

def is_connected():
    return 'user_connect' in session

def is_admin():
    return 'user_connect' in session and session['user_connect']['role'] == 'admin'

def is_customer():
    return 'user_connect' in session and session['user_connect']['role'] == 'customer'

def is_distributeur():
    return 'user_connect' in session and session['user_connect']['role'] == 'distributeur'