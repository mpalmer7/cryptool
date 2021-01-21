"""
When adding a new cipher:
1) add to argparse
2) add values to cryptanalyzer
3) add to list under cryptanalyzer
4) update readme
"""
import argparse
# import shutil  # used in print_plaintext

from LanguageVerifier import Language
import cryptanalyzer

# columns, lines = shutil.get_terminal_size((80, 20))
# COLBAR = "#" * columns

CIP_ARGS_BLACKLIST = ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]
ENGLISH = Language("en_US")  # TODO - language hardcoded to be English

# Command Line Arguments
parser = argparse.ArgumentParser()
# Positional argument: 'input'
parser.add_argument('input', help='input filepath or string', type=str)
# Optional (but required) argument: specify input type
parser.add_argument('-s', '--string', help='string input', action='store_true')
parser.add_argument('-f', '--file', help='file input', action='store_true')
# Optional (but required) argument: encrypt or decrypt the input
parser.add_argument('-e', '--encrypt', help='encrypt the input', action='store_true')
parser.add_argument('-d', '--decrypt', help='decrypt the input', action='store_true')
# Optional Flags: ciphers (if none provided, tries all)
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
def decrypt_ciphertext(inp_obj, cipher):
    for unverified_decrypted_text in __import__('ciphers.' + cipher, fromlist=['*']).decrypt(inp_obj):
        if unverified_decrypted_text:
            yield unverified_decrypted_text


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


def guess_cipher(inp_obj):
    cracking_order = cryptanalyzer.cryptanalysis(inp_obj.string)[0]
    for cipher in cracking_order:
        # print("checking: %s" % cipher)
        for unverified_decrypted_text in decrypt_ciphertext(inp_obj, cipher):
            # print("unverified: " + unverified_decrypted_text)
            if ENGLISH.verify_string(unverified_decrypted_text):  # TODO - hardcoded english
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


def parse_user_input():
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

    return CipherText(inp, key=args.key)


def main():
    requested_ciphers = [arg for arg in args.__dict__ if arg not in CIP_ARGS_BLACKLIST and args.__dict__[arg]]

    # 1. TAKE USER INPUT (FILE or STRING) -----------------------------------------------------------------------------#
    inp_obj = parse_user_input()

    # 2. DECRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    if args.decrypt:
        # a. Cipher is specified:
        if requested_ciphers:
            for cipher in requested_ciphers:
                print(f"Decrypting with {cipher}:")
                for unverified_decrypted_text in decrypt_ciphertext(inp_obj, cipher):
                    print(f"\t{unverified_decrypted_text}")
                print("")
        # b. Otherwise, have to guess the cipher:
        else:
            print("Attempting to guess the cipher...")
            plaintext = guess_cipher(inp_obj)
            if plaintext:
                print(f"Your ciphertext was decrypted as:\n\t{plaintext}")
                return plaintext
            else:
                print("Failed to decrypt: %s" % inp_obj.bytes)  # ToDo add press any key for acknowledgement
                return None

    # 3. ENCRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
    elif args.encrypt:
        if requested_ciphers:
            for cipher in requested_ciphers:
                ciphertext = encrypt_cipher(cipher, inp_obj)

                print(f"Here is your message encrypted with {cipher}:")
                print(f"\t{ciphertext}")
                return ciphertext
        else:
            InputError("no cipher specified to encrypt with!")

    # 4. EN/DECRYPT NOT SPECIFIED; QUIT -------------------------------------------------------------------------------#
    else:
        InputError("please specify to encrypt (-e) or decrypt (-d) input")


if __name__ == "__main__":
    main()
