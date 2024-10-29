import hashlib

def login():
    
    with open('config.ini', 'r+') as txtFile:
        
        lines = txtFile.readlines()  

        if not lines:  
            print('Welcome to Crypty')
            pwd = input('Enter a new password: ')
            confpwd = input('Confirm password: ')
            if pwd == confpwd:
                
                hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
                txtFile.write(hashed_pwd + '\n')  
                print("Password saved successfully.")
            else:
                print('Passwords do not match')
        else:
            print('Welcome to Crypty')
            pwd = input('Enter your password: ')
            entered_hash = hashlib.sha256(pwd.encode()).hexdigest()
            
            
            stored_hash = lines[0].strip()  
            
            if entered_hash == stored_hash:
                print("Log in successful")
                return True
            else:
                print("Incorrect password")
                return False

