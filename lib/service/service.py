from cryptography.fernet import Fernet
key_encrypt = b'1Q7ZeWaZoMBkU9xpKV-u9GTOybTNQdmmgG9G0wQVKKU='  
def encrypt_password(password):
    f = Fernet(key_encrypt)
    return f.encrypt(password.encode())
def decrypt_password(password):
    f = Fernet(key_encrypt)
    return f.decrypt(password).decode()

