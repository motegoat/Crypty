# Crypty

## Overview
Crypty is a powerful and user-friendly command-line application designed for encrypting and decrypting files. With its intuitive interface and robust security features, Crypty ensures that your sensitive information remains safe from prying eyes. 

## Features
- **File Encryption**: Securely encrypt any file with a strong encryption key.
- **File Decryption**: Effortlessly decrypt previously encrypted files.
- **Progress Bar**: Enjoy a visual progress bar for both encryption and decryption processes.
- **Password Protection**: Register and log in with a secure password to access the application.
- **Key Management**: Automatically generate and store encryption keys, or load existing ones.
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux.

## Installation

### Prerequisites
Make sure you have Python 3.6 or higher installed on your machine. You will also need the following Python libraries:

- `cryptography`
- `InquirerPy`
- `colorama`
- `prompt_toolkit`

You can install the required libraries using pip:

```bash
pip install cryptography InquirerPy colorama prompt_toolkit
```
###Clone the Repository

Clone this repository to your local machine:
```bash
git clone https://github.com/motegoat/Crypty.git
cd Crypty
```

##Usage
**Run the Application:** Start the Crypty application by executing the following command in your terminal:

```bash
python main.py
```
##Login or Register:

If it's your first time, you will need to register a new password.
If you already have an account, log in using your password.
Choose an Action: You can choose to encrypt or decrypt a file. The application will guide you through the process.

**Select a File:** A file dialog will appear for you to select the file you wish to encrypt or decrypt.

**Progress Display:** A progress bar will show you the status of the encryption or decryption process.

**Completion Message:** Once the process is complete, you will receive a message indicating the success or failure of the operation.