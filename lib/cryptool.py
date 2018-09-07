"""
When adding a new cipher:
1) add to argparse
2) add to cryptool main under arg flags
3) add to cryptool main under encryption
4) add values to cryptanalyzer
5) add to list under cryptanalyzer
6) update readme
"""
import argparse
import shutil  # used in print_plaintext

try:
    import cryptanalyzer

    found_cryptanalyzer = True
except ModuleNotFoundError:
    print("Cryptanalyzer package not found.")
    found_cryptanalyzer = False

try:
    import Verify
except ModuleNotFoundError:
    print("Verify package not found.")
# should probably do something then...

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file or string', type=str)
parser.add_argument('-s', '--string', help='string of ciphertext', action='store_true')
parser.add_argument('-f', '--file', help='text file of ciphertext', action='store_true')
parser.add_argument('-e', '--encrypt', help='Encrypting or Decrypting?', action='store_true')
parser.add_argument('-d', '--decrypt', help='Encrypting or Decrypting?', action='store_true')
# optional flags
parser.add_argument('-key', '--key', help='decryption/encryption key, if given', action='store_true')

parser.add_argument('-caesar', '--caesar', help='Caesar Cipher', action='store_true')
parser.add_argument('-binary', '--binary', help='convert binary to plaintext', action='store_true')
parser.add_argument('-b64', '--base64', help='Base64', action='store_true')
parser.add_argument('-morse', '--morse', help='Morse Code (-.)', action='store_true')
parser.add_argument('-sbyteXOR', '--singlebyteXOR', help='Single Byte XOR', action='store_true')
parser.add_argument('-ssub', '--simplesub', help='Substitution Cipher (WIP)', action='store_true')
parser.add_argument('-atb', '--atbash', help='Atbash Cipher', action='store_true')
parser.add_argument('-rhs', '--hashsearch', help='search Bing for a hash', action='store_true')
parser.add_argument('-revtext', '--reversetext', help='Reverse a string', action='store_true')
parser.add_argument('-vig', '--vigenere', help='Vigenère cipher', action='store_true')
args = parser.parse_args()

if args.key:
    key = input("Please enter the key: ")
else:
	key = None

def print_plaintext(plaintext_list):
    columns, lines = shutil.get_terminal_size((80, 20))
    for item in plaintext_list:
        print("#" * columns + "Cipher Text:\n\t" + item[2] + "\nCipher:\n\t" + item[0] + "\nPlaintext:")
        if len(item[1]) == 0:
            print("\tDECRYPTION FAILED")
        else:
            for i in item[1]:
                print("\t%s" % i)
    print("#" * columns)
    return None


def encrypt_cipher(cipher, inp):
    opt = __import__('ciphers.' + cipher, fromlist=['*']).encrypt(inp)
    return opt


def check_cipher(cipher, cipher_str, key=None, gc=False):
    # get the file of a given cipher and attempt to decrypt it using that module
    opt = __import__('ciphers.' + cipher, fromlist=['*']).decrypt(cipher_str, key)
    # If cipher isn't given, check if output is in English
    if gc is False:
        ppd = Verify.verify_all(opt)  # potential plaintext dictionary
    else:
        ppd = opt

    # verify with the user that the decryption method worked
    if ppd != {}:
        print("Did the %s decryption work? Output:" % cipher)
        for str in ppd:
            print(str)
        while 1 == 1:  # I realize this is ugly
            temp = input("(Y/N): ")
            if temp.lower() == "n":
                return None
            elif temp.lower() == "y":  # decryption sucessful
                return [cipher, ppd, cipher_str]  # [the cipher, the plaintext, and the original ciphertext]


# When a flag specifies the decryption cipher to use
def given_cipher(cipher, ctext_list, key=None):
    plaintext_list = []
    for ct in ctext_list:
        checker = check_cipher(cipher, ct, key, gc=True)
        if checker is not None:
            plaintext_list.append(checker)
        else:
            (plaintext_list.append([cipher, ["COULD NOT DECRYPT"], ct]))
    print_plaintext(plaintext_list)
    exit()


def main():
    # Take user input (file or string)
    inp_ciphers_list = []
    if args.string:
        inp_ciphers_list.append(args.input)
    elif args.file:  # Edit this pending input... currently reads line by line
        with open(args.input, 'r') as file:
            icl = file.readlines()
            for c in icl:
                inp_ciphers_list.append(c[:-1])  # removes '\n'
    else:
        print("please specify -s or -f for a string or file input")
        print("Example usage: ./cryptool.py [input] -sd [cipher flag]")
        exit()

    # Encrypt or decrypt input
    # TODO issue here, what if put multiple flags for ciphers.  It would run them in this order...
    if args.decrypt:
        # If given cipher
        # this can be simplified...
        if args.binary:
            given_cipher("binary", inp_ciphers_list)
        elif args.caesar:
            given_cipher("caesar", inp_ciphers_list, key)
        elif args.base64:
            given_cipher("b64", inp_ciphers_list)
        elif args.morse:
            given_cipher("morse", inp_ciphers_list)
        elif args.singlebyteXOR:
            given_cipher("singlebyteXOR", inp_ciphers_list)
        elif args.simplesub:
            given_cipher("simplesub", inp_ciphers_list)
        elif args.atbash:
            given_cipher("atbash", inp_ciphers_list)
        elif args.hashsearch:
            given_cipher("hashsearch", inp_ciphers_list)
        elif args.reversetext:
            given_cipher("reversetext", inp_ciphers_list)
        elif args.vigenere:
            given_cipher("vigenere", inp_ciphers_list, key)
        # otherwise, guess what cipher to use
        else:
            plaintext = []
            for cipher_str in inp_ciphers_list:
                # Guess what kind of cipher the input is, rank results
                if found_cryptanalyzer:
                    cracking_order = cryptanalyzer.cryptanalysis(cipher_str)[0]
                else:
                    # Arbitrary
                    cracking_order = ["binary", "b64", "morse", "singlebyteXOR", "subtypeciphers", "hashsearch"]

                # Will attempt to decrypt using the ranking of ciphers; stops when successful
                failed_to_crack = True
                for cipher in cracking_order:
                    # Decrypts file using a cipher, also checks if plaintext is in english
                    checker = check_cipher(cipher, cipher_str, key)
                    if checker is not None:
                        plaintext.append(checker)
                        failed_to_crack = False
                        break

                # else, decryption failed
                if failed_to_crack:
                    ppd = Verify.verify_cipher(cipher_str)
                    if not ppd:
                        plaintext.append(["FAILED", "", cipher_str])
                    else:
                        plaintext.extend(ppd)

            # print findings to Terminal
            print_plaintext(plaintext)
        exit()

    elif args.encrypt:
        if args.file:
            print("File will be encrypted line by line.")
        opt = []

        if args.binary:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("binary", inp))
        elif args.caesar:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("caesar", inp))
        elif args.base64:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("b64", inp))
        elif args.morse:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("morse", inp))
        elif args.singlebyteXOR:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("singlebyteXOR", inp))
        elif args.simplesub:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("simplesub", inp))
        elif args.atbash:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("atbash", inp))
        elif args.hashsearch:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("hashsearch", inp))
        elif args.reversetext:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("reversetext", inp))
        elif args.vigenere:
            for inp in inp_ciphers_list:
                opt.append(encrypt_cipher("vigenere", inp))
        else:
            print("Please specify a cipher to encrypt with.")
            print("Example usage: ./cryptool.py [input] -es -caesar")
            exit()
        print(opt) # work in progress
        exit()


    else:
        print("please specify -e or -d for encryption or decryption")
        print("Example usage: ./cryptool.py [input] -sd [optional flags]")
        exit()


if __name__ == '__main__':
    print("--CipherTool V.0.30--")
    main()
