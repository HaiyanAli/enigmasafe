from cryptography.fernet import Fernet
import hashlib
import os
import sqlite3
import pyperclip
import time
from rich.table import Table
from rich.console import Console
import pyperclip as pc
import string
import random


def error(e):
    print(e)




def copy(msg):
    try:
        pyperclip.copy(str(msg))
        print("password Copyed!")
        return True
    except Exception as e:
        error(e,"\nSome Thing we can copy password to Clipboard")
        return False
        
    

def get_key(password):
    key = 'RQnv4fQfP6-UAd6_9mF4LMQmXCO8VqQXy_tnO3q1DKY'
    password = hashlib.md5(password.encode()).hexdigest()
    key = key[:-len(password)]
    key = key+password+'='
    return key



def encrypt_file(file_path, key):
    fernet = Fernet(key)
    if os.path.exists(file_path):
        print("Encrypting File ....")
        time.sleep(1)
        with open(file_path, 'rb') as f:
            data = f.read()
        data = fernet.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(data)
        print("Done!!")
        return True
    else:
        print("Invalid-File Path")
        return False



def decrypt_file(file_path, key):
    fernet = Fernet(key)
    if os.path.exists(file_path):
        print("Decrypting File ....")
        time.sleep(1)
        with open(file_path, 'rb') as f:
            data = f.read()
        data = fernet.decrypt(data)
        with open(file_path, 'wb') as f:
            f.write(data)
        print("Done!!")
        return True
    else:
        print("Invalid-File Path")
        return False



def add_login_cred():
    while True:
        password = input('Set New Password: ')
        c_password = input('Confirm New Password: ')
        if password == c_password:
            break
        print('In-valid Password, Try Again!')
    
    password = hashlib.sha256(password.encode()).hexdigest()
    Connection = sqlite3.connect('data_base.db')
    cursor = Connection.cursor()
    query = f"INSERT INTO login_cred VALUES ('{password}')"
    cursor.execute(f"DELETE FROM login_cred")
    cursor.execute(query)
    Connection.commit()
    Connection.close()
    print("Password has been set!\n")
    return True



def generate_default_dataBase():
    if not os.path.exists('data_base.db'):
        sqliteConnection = sqlite3.connect('data_base.db')
        cursor = sqliteConnection.cursor()
        table1 = """ CREATE TABLE passwords (
                ID  INTEGER PRIMARY KEY AUTOINCREMENT,
                Name CHAR(255) NOT NULL,
                Description CHAR(500),
                Password CHAR(1500) NOT NULL
                    ); """
        table2 = """ CREATE TABLE login_cred (
                Password CHAR(500) NOT NULL
                    ); """
        
        try:
            cursor.execute(table1)
            cursor.execute(table2)
            print("Default data-base has been created!!")
            add_login_cred()
            return True
        except Exception as e:
            error(e)
            print("Some thing wrong we can create Default data-base!!")
            return False
    else:
        return None



def add_password(key):
    print("Lets add Password to data-base!")
    while True:
        name = input("Enter password Name: ")
        if name != '' or name != ' ':
            break
        print('Please enter password name!')
    while True:
        password = input("Enter password: ")
        if password != '' or password != ' ':
            break
        print('Please enter password!')
    desc = input('Enter Password Desciption: ')
    if desc == '':
        desc = 'none'


    fernet = Fernet(key)
    password = fernet.encrypt(password.encode())
    Connection = sqlite3.connect('data_base.db')
    cursor = Connection.cursor()
    query = f"INSERT INTO passwords (Name, Description, Password) VALUES ('{name}', '{desc}','{password.decode()}')"
    try:
        cursor.execute(query)
        Connection.commit() 
        Connection.close()
        print("Password has been added")
        return True
    except Exception as e:
        error(e)
        return False



def show_passwords():
    print()
    Connection =sqlite3.connect('data_base.db')
    cursor = Connection.cursor()
    cursor.execute("SELECT * FROM passwords")
    data = cursor.fetchall()

    if 1 != 1 :
        print("Data Not-Found!")
        return

    table = Table(title="Passwords Lists")
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Description')
    for i in data:
        table.add_row(str(i[0]),i[1],i[2], style='bright_green')

    console = Console()
    console.print(table)    



def get_password(key, password_id):
    Connection = sqlite3.connect('data_base.db')
    cursor = Connection.cursor()
    query = f"SELECT * FROM passwords WHERE ID = {password_id}"
    cursor.execute(query)
    try:
        data = cursor.fetchall()[0]
    except:
        return False
    id = data[0]
    name = data[1]
    desc = data[2]
    password = data[3]
    fernet = Fernet(key)
    password = fernet.decrypt(password.encode()).decode()
    pc.copy(password)
    print()
    print(f"{name} password copyed!")



def login():
    password = input("Enter Login Password: ")
    v_passsword = hashlib.sha256(password.encode()).hexdigest()
    Connection = sqlite3.connect('data_base.db')
    cursor = Connection.cursor()
    query = f"SELECT * FROM login_cred "
    cursor.execute(query)
    try:
        data = cursor.fetchall()[0]
    except Exception as e:
        error(e)
        return False
    if v_passsword == data[0]:
        return get_key(password)
    else:
        print("In-Valid Login Password!")
        return False
    


def password_generater(arg = 'lucd'):
    arg = arg.lower()
    if 'l' not in arg and 'u' not in arg and 'c' not in arg and 'd' not in arg:
        print(f'In-valid option! [{arg}]')
        return
    main_list=[]
    if 'l' in arg:
        main_list = main_list + list(string.ascii_lowercase)
    if 'u' in arg:
        main_list = main_list + list(string.ascii_uppercase)
    if 'c' in arg:
        main_list = main_list + list(string.punctuation)
    if 'd' in arg:
        main_list = main_list + list(string.digits)
    
    while True:
        paslen = input("Enter password length [Default=13]: ")
        if paslen == '' or paslen == ' ':
            paslen = '13'
            break
        elif not paslen.isdigit():
            print("In-valid: Enter only number please!")
        elif int(paslen) < 8:
            print("Warning: This length is to short, Please select between 8 to 64")
        elif int(paslen) > 64:
            print("Warning: This length is to long, Please select between 8 to 64")
        else:
            break
    
    password = ''.join(random.choice(main_list) for _ in range(int(paslen)))
    print(f"Your Password is '{password}'")
    


