from config import FERNET

# Utility functions for Encryption and Decryption
def encrypt(data):
    cipher_suite = FERNET
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt(data):
    cipher_suite = FERNET
    decrypted_data = cipher_suite.decrypt(data).decode()
    return decrypted_data
