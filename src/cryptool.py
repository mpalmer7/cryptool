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

columns, lines = shutil.get_terminal_size((80, 20))
COLBAR = "#" * columns

# Command Line Arguments
parser = argparse.ArgumentParser()
# Positional argument: 'input'
parser.add_argument('input', help='input filepath or string', type=str)
# Optional (but required) argument: specify input type
parser.add_argument('-s', '--string', help='string input', action='store_true')
parser.add_argument('-f', '--file', help='file input', action='store_true')
# Optional (but required) argument: encrypt or decrypt the input?
parser.add_argument('-e', '--encrypt', help='encrypt the input', action='store_true')
parser.add_argument('-d', '--decrypt', help='decrypt the input', action='store_true')
# Optional Flags: ciphers (if blank, tries all by default)
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
parser.add_argument('-steg', '--steg', help="Steganography", action='store_true')
# Optional Flags: other
parser.add_argument('-key', '--key', help='specify a key', type=str)
parser.add_argument('-cic', '--cipherincipher', help='check for encryption with multiple ciphers', action='store_true')

args = parser.parse_args()


class InputError:
    def __init__(self, err):
        print("ERROR WITH INPUT: %s" % err)
        print("Example usage: ./cryptool.py [input] -d -f [optional flags]")
        exit()


class CipherText:
    def __init__(self, inp, key=None):
        if isinstance(inp, str):
            self.string = inp
            self.bytes = inp.encode()
        elif isinstance(inp, bytes):
            self.string = inp.decode('utf-8')
            self.bytes = inp
        else:
            InputError("familiar format (not bytes or string)" % inp)

        self.key = key


# run the decrypt function of a given cipher, this function by convention attempts to decrypt the cipher-text
# this function by convention attempts to decrypt the cipher-text, and will yield any results
def decrypt_ciphertext(inp_obj, cipher, key=None):
    for unverified_decrypted_text in __import__('ciphers.' + cipher, fromlist=['*']).decrypt(inp_obj):
        if unverified_decrypted_text:
            yield unverified_decrypted_text


def verify_plaintext(potential_plaintext, language_obj):
    verified_boo = LanguageVerifier.verify_string(potential_plaintext, language_obj)
    return verified_boo


def get_user_feedback(cipher, plaintext):
    print("Did the %s decryption work? ('X' to not try again)" % cipher)
    print(plaintext)
    temp = input("(Y/N/X): ")
    if temp.lower() == "n":
        return 0
    elif temp.lower() == "y":
        return 1
    elif temp.lower() == "x":
        return 2
    else:
        print("Response not understood...\n")
        return get_user_feedback(cipher, plaintext)


def guess_cipher(inp_obj, lang_obj):
    cracking_order = cryptanalyzer.cryptanalysis(inp_obj.string)[0]
    for cipher in cracking_order:
        # print("checking: %s" % cipher)
        for unverified_decrypted_text in decrypt_ciphertext(inp_obj, cipher):
            if verify_plaintext(unverified_decrypted_text, lang_obj):
                machine_verified_decrypted_text = unverified_decrypted_text
                res = get_user_feedback(cipher, machine_verified_decrypted_text)
                if res == 2:
                    return False
                if res == 1:
                    human_verified_decrypted_text = machine_verified_decrypted_text
                    return human_verified_decrypted_text
    return False


def encrypt_cipher(cipher, inp_obj):
    return __import__('ciphers.' + cipher, fromlist=['*']).encrypt(inp_obj)


def main():
    # 1. TAKE USER INPUT (FILE or STRING) -----------------------------------------------------------------------------#
    inp = None
    if args.string:
        inp = args.input
    elif args.file:
        try:
            with open(args.input, 'rb') as file:
                inp = file.read()
        except FileNotFoundError:
            InputError("specified file path not found ('%s')" % args.input)
    else:
        InputError("please specify input type as string (-s) or file (-f)")

    inp_obj = CipherText(inp, key=args.key)

    # TODO issue here, what if put multiple flags for ciphers.  It would run them in order; just one...
    # 2. DECRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    if args.decrypt:
        # a. If cipher is specified:
        for arg in args.__dict__:  # ToDo change to parent/child argparse to not need to do this
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]:
                if args.__dict__[arg]:
                    print("Decrypted %s as:" % inp_obj.bytes)
                    for plaintext in decrypt_ciphertext(inp_obj, arg):  # arg is cipher name
                        print("\t" + plaintext)
                    exit()

        # b. Otherwise, have to guess what cipher it is:
        json_opt = {}

        lang_obj = LanguageVerifier.Language("english")  # ToDo hardcoded for english
        decrypted_cipher = guess_cipher(inp_obj, lang_obj)
        if decrypted_cipher:
            json_opt[inp_obj.bytes] = decrypted_cipher
        else:
            print(COLBAR, end='')
            print("Failed to decrypt: %s" % inp_obj.bytes)  # ToDo add press any key for acknowledgement
            json_opt[inp_obj.bytes] = "FAILED TO DECRYPT"

        print("\n\nFINAL JSON OPT:\n\n")
        print(json_opt)
        exit()

    # 3. ENCRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    elif args.encrypt:
        for arg in args.__dict__:  # locate what user specified to encrypt with
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]:
                if args.__dict__[arg]:
                    print("Here is your encrypted message: ")
                    print(encrypt_cipher(arg, inp_obj))
                    exit()
        InputError("no cipher specified to encrypt with")
    # 4. NOT SPECIFIED; QUIT ------------------------------------------------------------------------------------------#
    else:
        InputError("please specify to encrypt (-e) or decrypt (-d) input")


if __name__ == "__main__":
    main()
