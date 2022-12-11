import argparse
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='the file to encrypt/decrypt')
    parser.add_argument('-k', '--key', help='the rsa key to use')
    parser.add_argument('-g', '--generate', action='store_true', help='generate a new rsa key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt the file')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt the file')
    args = parser.parse_args()
    encrypted_key = None

    if args.filename == None and args.key == None and not args.generate and not args.decrypt and not args.encrypt:
        print("Error: No arguments given.")
        print("Use -h or --help for help.")
        exit(1)

    if args.encrypt and args.decrypt:
        print("Error: You cannot use -e and -d at the same time.")
        exit(1)

    if args.generate and args.key != None or args.generate and args.filename != None or args.generate and args.decrypt or args.generate and args.encrypt:
        print("Error: You cannot use -g and any other arguments at the same time.")
        exit(1)

    if args.filename == "" or args.key == "":
        print("Error: No file specified.")
        exit(1)
    
    if args.key != None and args.filename == None or args.decrypt and args.filename == None or args.encrypt and args.filename == None:
        print("Error: You must specify a file to encrypt/decrypt.")
        exit(1)

    if args.filename != None and args.key == None:
        print("Error: You must specify a key to encrypt/decrypt with.")
        exit(1)
        
    if args.filename != None and args.key != None and not args.decrypt and not args.encrypt:
        print("Error: You must specify whether to encrypt or decrypt the file.")
        exit(1)

    if args.key:
        try:
            with open(args.key, "rb") as f:
                encrypted_key = f.read()
        except FileNotFoundError:
            print("Error: RSA key not found.")
            exit(1)

    if args.generate:
        secret = input("Enter a passphrase: ")
        key = RSA.generate(3072)
        encrypted_key = key.export_key(passphrase=secret, pkcs=8, protection="scryptAndAES128-CBC")
        filename = str(input("Enter a filename to save the key to: "))
        if filename == "":
            filename = "rsa"
        with open(filename + ".key", "wb") as f:
                f.write(encrypted_key)
        print("Key saved as " + filename + ".key")

    if args.decrypt and args.key and args.filename:
        decrypt(args.filename, encrypted_key)

    if args.encrypt and args.key and args.filename:
        encrypt(args.filename, encrypted_key)
    
def decrypt(filename, key):
    try:
        with open(filename, "rb") as f:
            encrypted = f.read()
    except FileNotFoundError:
        print("Error: File not found.")
        exit(1)
    secret = input("Enter the passphrase: ")
    try:
        key = RSA.import_key(key, passphrase=secret)
    except ValueError:
        print("Error: Wrong passphrase.")
        exit(1)
    cipher = PKCS1_OAEP.new(key)
    try:
        decrypted = cipher.decrypt(encrypted)
    except ValueError:
        print("Error: Wrong RSA key for this file.")
        exit(1)
    with open(filename, "wb") as f:
        f.write(decrypted)
    print("File decrypted successfully.")

def encrypt(filename, key):
    try:
        with open(filename, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: File not found.")
        exit(1)
    secret = input("Enter the passphrase: ")
    try:
        key = RSA.import_key(key, passphrase=secret)
    except ValueError:
        print("Error: Wrong passphrase.")
        exit(1)
    cipher = PKCS1_OAEP.new(key)
    try:
        encrypted = cipher.encrypt(data)
    except ValueError:
        print("Error: File is too large. Try a smaller file.")
        exit(1)
    with open(filename, "wb") as f:
        f.write(encrypted)
    print("File encrypted successfully.")

if __name__ == '__main__':
    main()