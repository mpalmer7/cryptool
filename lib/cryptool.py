"""
When adding a new cipher:
1) add to argparse
2) add values to cryptanalyzer
3) add to list under cryptanalyzer
4) update readme
"""
import shutil  # used in print_plaintext
import cryptanalyzer
import Verify
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file or string', type=str)
parser.add_argument('-s', '--string', help='string input', action='store_true')
parser.add_argument('-f', '--file', help='file input', action='store_true')
parser.add_argument('-e', '--encrypt', help='encrypt the input', action='store_true')
parser.add_argument('-d', '--decrypt', help='decrypt the input', action='store_true')
parser.add_argument('-key', '--key', help='specify a key', type=str)
parser.add_argument('-cic', '--cipherincipher', help='check for encryption with multiple ciphers', action='store_true')  # ToDo
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
parser.add_argument('-vig', '--vigenere', help='Vigenère cipher (needs key)', action='store_true')
args = parser.parse_args()

key = args.key


class InputError:
    def __init__(self, err):
        print("ERROR with input formatting of: %s" % err)
        print("Example usage: ./cryptool.py [input] -d -f [optional flags]")
        exit()


def print_plaintext(plaintext_list):
    columns, lines = shutil.get_terminal_size((80, 20))
    for item in plaintext_list:
        print("#" * columns + "\nCipher Text:\n\t" + item[2] + "\nCipher:\n\t" + item[0] + "\nPlaintext:")
        if len(item[1]) == 0:
            print("\tDECRYPTION FAILED")
        else:
            for i in item[1]:
                print("\t%s" % i[0])
    print("#" * columns)
    return None


def check_cipher(cipher, cipher_str, key=None, gc=False):
    # get the file of a given cipher and attempt to decrypt it using that module
    opt = __import__('ciphers.' + cipher, fromlist=['*']).decrypt(cipher_str, key)
    inv = []
    if gc:  # cipher is given
        for o in opt:
            inv.append([o, "Unverified"])
    else:
        inv = Verify.verify_all(opt, args.cipherincipher)

    if inv == [] or inv is None:
        return None

    print("Did the %s decryption work? Output:" % cipher)
    for plaintext, ver_type in inv:
        if ver_type not in ["English", "Unverified"]:
            print("Cipher within a cipher found: " + ver_type)
        print(plaintext)

    while 1 == 1:  # TODO ugly
        temp = input("(Y/N): ")
        if temp.lower() == "n":
            return None
        elif temp.lower() == "y":  # decryption successful
            return [cipher, inv, cipher_str]  # [the cipher, the plaintext(s), and the original ciphertext]


# When a flag specifies the decryption cipher to use
def given_cipher(cipher, ctext_list, key=None):
    plaintext_list = []
    for ct in ctext_list:
        checker = check_cipher(cipher, ct, key, gc=True)
        if checker is not None:
            plaintext_list.append(checker)
        else:
            (plaintext_list.append([cipher, ["COULD NOT DECRYPT"], ct]))
    return plaintext_list


def guess_cipher(inp_list):
    plaintext_list = []
    for cipher_str in inp_list:
        failed_to_crack = True

        # Guess what kind of cipher the input is, returns ranked results
        cracking_order = cryptanalyzer.cryptanalysis(cipher_str)[0]

        # Will attempt to decrypt using the ranking of ciphers; stops when successful
        for cipher in cracking_order:
            # Decrypts file using a cipher, also checks if plaintext is in english
            checker = check_cipher(cipher, cipher_str, key)
            if checker is not None:
                plaintext_list.append(checker)
                failed_to_crack = False
                break

        # else, decryption failed
        if failed_to_crack:
            plaintext_list.append(["FAILED", "", cipher_str])

    return plaintext_list


def encrypt_cipher(cipher, inp):
    return __import__('ciphers.' + cipher, fromlist=['*']).encrypt(inp, key)


def main():
    # 1. TAKE USER INPUT (FILE OR STRING) -----------------------------------------------------------------------------#
    inp_list = []
    if args.string:
        inp_list.append(args.input)
    elif args.file:
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
        for arg in args.__dict__:
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key", "cipherincipher"]:
                if args.__dict__[arg]:
                    print_plaintext(given_cipher(arg, inp_list, key))
                    exit()
        # b. Otherwise, have to guess what cipher it is:
        print_plaintext(guess_cipher(inp_list))

    # 2. ENCRYPT FILE; IF SPECIFIED -----------------------------------------------------------------------------------#
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

    # 3. NOT SPECIFIED; QUIT ------------------------------------------------------------------------------------------#
    else:
        InputError("encrypt or decrypt")


if __name__ == "__main__":
    main()