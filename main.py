import hashlib
import os 
from prompt_toolkit.formatted_text import FormattedText
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
from InquirerPy import inquirer
from InquirerPy import prompt
import time
from colorama import Fore, Back, Style


def login():
    if not os.path.isfile('config.ini'):
        filemode = 'w+'
    else: 
        filemode = 'r+'


    with open('config.ini', filemode) as txtFile:
        
        lines = txtFile.readlines()  

        if not lines:  
            register()
        else:
            print('Welcome to Crypty')
            pwd = inquirer.text(message="Enter your password: ", is_password=True).execute()
            entered_hash = hashlib.sha256(pwd.encode()).hexdigest()
            
            
            stored_hash = lines[0].strip()  
            
            if entered_hash == stored_hash:
                print(Fore.GREEN +  "Log in successful")
                print(Style.RESET_ALL)

                return True
            else:
                print(Fore.RED + "Incorrect password")
                print(Style.RESET_ALL)
                return False

def register():
    txtFile = open('config.ini', 'r+') 
    print('Welcome to Crypty')
    pwd = inquirer.text(message="Enter new password: ", is_password=True).execute()
    confpwd = inquirer.text(message="Confirm new password: ", is_password=True).execute()
    if pwd == confpwd:
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
        txtFile.write(hashed_pwd + '\n')  
        print(Fore.GREEN + "Password saved successfully.")
        key = generate_enckey()
        os.system('cls')
        return True
    else:
        print(Fore.RED + 'Passwords do not match')
        print(Style.RESET_ALL)
        return False

def open_file():
    
    root = tk.Tk()
    root.withdraw()  
    root.attributes("-topmost", True)  

    return filedialog.askopenfilename()

def generate_enckey():
    key = Fernet.generate_key()
    with open("key.AES", "wb") as key_file:
        key_file.write(key)
    return key

def load_key(): 
    if not os.path.isfile('key.AES'): 
        print(Fore.RED + 'Encryption key not found ')
        print(Fore.RED + 'ERROR: 404')
        print(Style.RESET_ALL)
        confkeyreset = {
            "name":"generate_key",
            "type": "list",
            "message": "Would you like to generate a new encrption key:",
            "choices": ["Yes", "No"],
            "default": None,
        }
        response = prompt([confkeyreset])
        if response['generate_key'] == "Yes":
            key_file =  open("key.AES", "w+")
            with open("key.AES", "wb") as key_file:
                key = Fernet.generate_key()
                key_file.write(key)
                return key
        else:
            print('This program is unusable without a encryption key')
            time.sleep(5)

    else:
        with open("key.AES", "rb") as key_file:
            key = key_file.read()
        return key
        

if login():
    
    print(load_key())
    
