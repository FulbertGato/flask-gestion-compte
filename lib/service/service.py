from cryptography.fernet import Fernet
key_encrypt = b'1Q7ZeWaZoMBkU9xpKV-u9GTOybTNQdmmgG9G0wQVKKU='  
def encrypt_password(password):
    f = Fernet(key_encrypt)
    return f.encrypt(password.encode())
def decrypt_password(password):
    f = Fernet(key_encrypt)
    return f.decrypt(password).decode()

def generate_account_number():
    from datetime import datetime
    time_data = datetime.now()
    date_time_str = time_data.strftime("%Y%m%d%H%M%S")
    return date_time_str
