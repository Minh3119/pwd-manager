import os
import io
import json
from cryptography.fernet import Fernet


def jsonFileCheck(path, file_name:str):
    """if os.path.isfile(path) and os.access(path, os.R_OK):
        return True
    else:
        with io.open(os.path.join(path, file_name), 'w') as db_file:
            if file_name == "bank.json":
                print("Rewriting file1")
                data = get_register_data()
                db_file.write(json.dumps(data))
            else:
                print("Rewriting file2")
                db_file.write(json.dumps({}))"""
    
    if not os.path.exists(file_name):
        if file_name == "bank.json":
            print("Rewriting file1")
            data = get_register_data()
            with open(file_name, "w") as json_file:
                json.dump(data, json_file)
        else:
            with open(file_name, "w") as json_file:
                json.dump({}, json_file)
            print("Rewriting file2")
    else:
        return


def encrypt_password(password):
    with open("bank.json", "r") as json_file:
        data = json.load(json_file)        
    cipher_suite = Fernet(data["key"].encode())
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password):
    with open("bank.json", "r") as json_file:
        data = json.load(json_file)
    cipher_suite = Fernet(data["key"].encode())
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

'''# Generate encryption key
key = Fernet.generate_key()

# Password to encrypt
password = "mysecretpassword"

# Encrypt the password
encrypted_password = encrypt_password(password, key)

# Store encrypted password in JSON file
data = {
    "encrypted_password": encrypted_password.decode()
}

with open("passwords.json", "w") as json_file:
    json.dump(data, json_file)'''

def get_register_data():
    master_pw = "default"
    key = Fernet.generate_key()
    data = {
        "master_pw" : master_pw,
        "key" : key.decode()
    }
    '''with open("bank.json", "w") as json_file:
        json.dump(data, json_file)'''
    return data

