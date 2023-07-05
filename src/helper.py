import os
import json
from cryptography.fernet import Fernet


def jsonFileCheck(path, file_name:str):    
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


def get_register_data():
    master_pw = "default"
    key = Fernet.generate_key()
    data = {
        "master_pw" : master_pw,
        "key" : key.decode()
    }
    return data

