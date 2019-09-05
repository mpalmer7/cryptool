"""
When adding a new cipher:
1) add to argparse
2) add values to cryptanalyzer
3) add to list under cryptanalyzer
4) update readme
"""
import argparse
import shutil  # used in print_plaintext

import LanguageVerifier
import cryptanalyzer

# Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file or string', type=str)
parser.add_argument('-s', '--string', help='string input', action='store_true')
parser.add_argument('-f', '--file', help='file input', action='store_true')
parser.add_argument('-e', '--encrypt', help='encrypt the input', action='store_true')
parser.add_argument('-d', '--decrypt', help='decrypt the input', action='store_true')
parser.add_argument('-key', '--key', help='specify a key', type=str)
parser.add_argument('-cic', '--cipherincipher', help='check for encryption with multiple ciphers', action='store_true')
# Optional Flags: ciphers
parser.add_argument('-caesar', '--caesar', help='Caesar Cipher', action='store_true')
parser.add_argument('-binary', '--binary', help='Binary-Plaintext Conversion', action='store_true')
parser.add_argument('-b64', '--base64', help='Base64', action='store_true')
parser.add_argument('-morse', '--morse', help='Morse Code (-.)', action='store_true')
parser.add_argument('-sbyteXOR', '--singlebyteXOR', help='Single Byte XOR', action='store_true')
parser.add_argument('-mono', '--monoalphabetic', help='Monoalphabetic Substitution Cipher', action='store_true')
parser.add_argument('-atb', '--atbash', help='Atbash Cipher', action='store_true')
parser.add_argument('-rhs', '--hash', help='search DuckDuckGo for a hash', action='store_true')
parser.add_argument('-revtext', '--reversetext', help='reverse the text', action='store_true')
parser.add_argument('-vig', '--vigenere', help='Vigenere cipher (needs key)', action='store_true')
parser.add_argument('-aes', '--aes', help="AES Cipher", action='store_true')
args = parser.parse_args()
key = args.key


class InputError:
    def __init__(self, err):
        print("ERROR with input formatting of: %s" % err)
        print("Example usage: ./cryptool.py [input] -d -f [optional flags]")
        exit()


columns, lines = shutil.get_terminal_size((80, 20))
COLBAR = "#" * columns


# run the decrypt function of a given cipher, this function by convention attempts to decrypt the cipher-text
# this function by convention attempts to decrypt the cipher-text, and will yield any results
def decrypt_ciphertext(ciphertext, cipher, key=None):
    for unverified_decrypted_text in __import__('ciphers.' + cipher, fromlist=['*']).decrypt(ciphertext, key):
        if unverified_decrypted_text:
            yield unverified_decrypted_text


def verify_plaintext(potential_plaintext, language_obj):
    verified_boo = LanguageVerifier.verify_string(potential_plaintext, language_obj)
    return verified_boo


def get_user_feedback(ciphertext, cipher, plaintext):
    print(COLBAR, end='')
    print(ciphertext)
    print("Did the %s decryption work? ('X' to not try again)" % cipher)
    print(plaintext)
    while 1 == 1:  # ToDo ugly
        temp = input("(Y/N/X): ")
        if temp.lower() == "n":
            return 0
        elif temp.lower() == "y":
            return 1
        elif temp.lower() == "x":
            return 2


def guess_cipher(ciphertext, lang_obj):
    cracking_order = cryptanalyzer.cryptanalysis(ciphertext)[0]
    for cipher in cracking_order:
        for unverified_decrypted_text in decrypt_ciphertext(ciphertext, cipher):
            if verify_plaintext(unverified_decrypted_text, lang_obj):
                machine_verified_decrypted_text = unverified_decrypted_text
                res = get_user_feedback(ciphertext, cipher, machine_verified_decrypted_text)
                if res == 2:
                    return False
                if res == 1:
                    human_verified_decrypted_text = machine_verified_decrypted_text
                    return human_verified_decrypted_text
    return False


def encrypt_cipher(cipher, inp):
    return __import__('ciphers.' + cipher, fromlist=['*']).encrypt(inp, key)


def main():
    # 1. TAKE USER INPUT (FILE OR STRING) -----------------------------------------------------------------------------#
    inp_list = []
    if args.string:
        inp_list.append(args.input)
    elif args.file:  # ToDo change to regex check then reading line-by-line
        print("File will be read line by line.")
        with open(args.input, 'r') as file:
            icl = file.readlines()
            for c in icl:
                inp_list.append(c[:-1])  # removes '\n'
    else:
        InputError("string or file")

    # TODO issue here, what if put multiple flags for ciphers.  It would run them in order; just one...
    # 2. DECRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    if args.decrypt:
        # a. If cipher is specified:
        for arg in args.__dict__:  # ToDo change to parent/child argparse to not need to do this
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]:
                if args.__dict__[arg]:
                    for ciphertext in inp_list:
                        print("Decrypted %s as:" % ciphertext)
                        for plaintext in decrypt_ciphertext(ciphertext, arg, key):  # arg is cipher name
                            print("\t"+plaintext)
                    exit()

        # b. Otherwise, have to guess what cipher it is:
        json_opt = {}
        for ciphertext in inp_list:
            lang_obj = LanguageVerifier.Language("english")  # ToDo hardcoded english
            decrypted_cipher = guess_cipher(ciphertext, lang_obj)
            if decrypted_cipher:
                json_opt[ciphertext] = decrypted_cipher
            else:
                print(COLBAR, end='')
                print("Failed to decrypt: %s" % ciphertext)  # ToDo add press any key for acknowledgement
                json_opt[ciphertext] = "FAILED TO DECRYPT"

        print("\n\nFINAL JSON OPT:\n\n")
        print(json_opt)
        exit()

    # 3. ENCRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    elif args.encrypt:
        if args.file:
            print("File will be encrypted line by line.")

        opt = []
        for arg in args.__dict__:  # locate what user specified to encrypt with
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]:
                if args.__dict__[arg]:
                    for inp in inp_list:
                        opt.append(encrypt_cipher(arg, inp))
                    print("Here is your encrypted message: ")
                    for o in opt:
                        print(o)
                    exit()
        InputError("no cipher specified to encrypt with")
    # 4. NOT SPECIFIED; QUIT ------------------------------------------------------------------------------------------#
    else:
        InputError("encrypt or decrypt")


if __name__ == "__main__":
    main()
