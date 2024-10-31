import hashlib
import os
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet, InvalidToken
from InquirerPy import prompt
import time
from colorama import Fore, Style
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
from tqdm import tqdm  # Make sure to install tqdm if you haven't already

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
            pwd = prompt([{
                "type": "password",
                "name": "password",
                "message": "Enter your password: "
            }])["password"]

            entered_hash = hashlib.sha256(pwd.encode()).hexdigest()
            stored_hash = lines[0].strip()  
            
            if entered_hash == stored_hash:
                print(Fore.GREEN + "Log in successful")
                print(Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + "Incorrect password")
                print(Style.RESET_ALL)
                return False


def register():
    print('Welcome to Crypty')
    pwd = prompt([{
        "type": "password",
        "name": "password",
        "message": "Enter new password: "
    }])["password"]
    
    confpwd = prompt([{
        "type": "password",
        "name": "confirm_password",
        "message": "Confirm new password: "
    }])["confirm_password"]

    if pwd == confpwd:
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
        with open('config.ini', 'w+') as txtFile:
            txtFile.write(hashed_pwd + '\n')  
        print(Fore.GREEN + "Password saved successfully.")
        print(Style.RESET_ALL)
        generate_enckey()
        purpose()
        return True
    else:
        print(Fore.RED + 'Passwords do not match')
        print(Style.RESET_ALL)
        purpose()
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
        response = prompt({
            "name": "generate_key",
            "type": "list",
            "message": "Would you like to generate a new encryption key:",
            "choices": ["Yes", "No"],
            "default": None,
        })
        if response['generate_key'] == "Yes":
            return generate_enckey()
        else:
            print('This program is unusable without an encryption key')
            time.sleep(5)
            return None

    with open("key.AES", "rb") as key_file:
        key = key_file.read()
    return key
        
def encrypt_file(file_path):
    key = load_key()
    if key is None:
        print(Fore.RED + "Error: Key loading failed." + Style.RESET_ALL)
        return  # Exit if key loading failed
    fernet = Fernet(key)

    # List of allowed file extensions
    allowed_extensions = ['.pdf', '.txt']

    # Check if the file is allowed
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        print(Fore.RED + "Error: Only .pdf and .txt files are supported for encryption." + Style.RESET_ALL)
        return

    # Debugging information
    print(f"Attempting to encrypt file: {file_path}")
    if not os.path.isfile(file_path):
        print(Fore.RED + "Error: The specified file does not exist." + Style.RESET_ALL)
        return

    file_size = os.path.getsize(file_path)
    print(f"Size of file to encrypt: {file_size} bytes")  # Log the size of the file
    chunk_size = 8192  # Chunk size for reading the file
    encrypted_path = file_path + ".enc"  # Append .enc to the file name

    try:
        with open(file_path, "rb") as original_file, open(encrypted_path, "wb") as encrypted_file:
            # Create a progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc="Encrypting") as pbar:
                for chunk in iter(lambda: original_file.read(chunk_size), b""):
                    encrypted_data = fernet.encrypt(chunk)
                    encrypted_file.write(encrypted_data)
                    pbar.update(len(chunk))  # Update progress bar

        print(f"File '{file_path}' has been encrypted as '{encrypted_path}'.")

    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred during encryption: {str(e)}" + Style.RESET_ALL)

def decrypt_file(file_path):
    key = load_key()
    if key is None:
        print(Fore.RED + "Error: Key loading failed." + Style.RESET_ALL)
        return  # Exit if key loading failed
    fernet = Fernet(key)

    # List of common video and audio file extensions
    blocked_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                          '.mpeg', '.mpg', '.mp3', '.wav', '.aac', '.ogg', 
                          '.flac', '.wma']

    # Check if the file is a video or audio
    if any(file_path.lower().endswith(ext) for ext in blocked_extensions):
        print(Fore.RED + "Error: Video and audio files are not supported for decryption." + Style.RESET_ALL)
        return

    # Debugging information
    print(f"Attempting to decrypt file: {file_path}")
    print(f"Using key: {key.decode()}")  # Print the key being used for decryption
    if not file_path.endswith(".enc"):
        print(Fore.RED + "Error: The file does not have the correct '.enc' extension." + Style.RESET_ALL)
        return

    file_size = os.path.getsize(file_path)
    print(f"Size of encrypted file: {file_size} bytes")  # Log the size of the file
    chunk_size = 8192  # Increased chunk size for video files
    decrypted_path = file_path[:-4]  # Remove the last 4 characters (".enc")

    try:
        with open(file_path, "rb") as encrypted_file, open(decrypted_path, "wb") as decrypted_file:
            # Create a progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc="Processing") as pbar:
                for _ in range(0, file_size, chunk_size):
                    chunk = encrypted_file.read(chunk_size)
                    if chunk:
                        decrypted_data = fernet.decrypt(chunk)
                        decrypted_file.write(decrypted_data)
                        pbar.update(len(chunk))  # Update progress bar

        print(f"File '{file_path}' has been decrypted as '{decrypted_path}'.")

    except InvalidToken:
        print(Fore.RED + "Error: Decryption failed. The file may be corrupted or the key is incorrect." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred during decryption: {str(e)}" + Style.RESET_ALL)

def purpose():
    while True:
        response = prompt({
            "name": "function",
            "type": "list",
            "message": "Would you like to: ",
            "choices": ["Encrypt", "Decrypt", "Exit"],
            "default": None,
        })
        if response['function'] == "Encrypt":
            encrypt_file(open_file())
        elif response['function'] == "Decrypt":
            decrypt_file(open_file())
        else:
            break 

if __name__ == "__main__":
    if login():
        purpose()
