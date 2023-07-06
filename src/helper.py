import os
import json
from cryptography.fernet import Fernet
import random
import string

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


smlLtrs = string.ascii_lowercase
capLtrs = string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation

set = [smlLtrs, numbers, symbols, capLtrs]


def gen_password():

    passwd = []
    # Making sure the generated password has all types of chars
    passwd += random.choice(smlLtrs)
    passwd += random.choice(capLtrs)
    passwd += random.choice(numbers)

    symbol_counter = 0

    letters = random.randint(10, 16)

    while symbol_counter < 3:
        temp = random.choice(symbols)
        if temp not in passwd:
            passwd.append(temp)
            symbol_counter += 1

    for i in range(letters - 6):
        chosen_set = random.choice(set)
        key = random.choice(chosen_set)
        passwd += key

    # Shuffling
    random.shuffle(passwd)

    # Converting to String
    final = ""
    for each in passwd:
        final += each

    return final

