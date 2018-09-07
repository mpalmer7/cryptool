"""
When adding a new cipher:
1) add to argparse
2) add values to cryptanalyzer
3) add to list under cryptanalyzer
4) update readme
"""
import argparse
import shutil  # used in print_plaintext
import cryptanalyzer
import Verify

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
    return __import__('ciphers.' + cipher, fromlist=['*']).encrypt(inp)


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
    return plaintext_list

def guess_cipher(inp_list):
    plaintext_list = []
    for cipher_str in inp_list:
        # Guess what kind of cipher the input is, rank results
        cracking_order = cryptanalyzer.cryptanalysis(cipher_str)[0]

        # Will attempt to decrypt using the ranking of ciphers; stops when successful
        failed_to_crack = True
        for cipher in cracking_order:
            # Decrypts file using a cipher, also checks if plaintext is in english
            checker = check_cipher(cipher, cipher_str, key)
            if checker is not None:
                plaintext_list.append(checker)
                failed_to_crack = False
                break

        # else, decryption failed
        if failed_to_crack:
            ppd = Verify.verify_cipher(cipher_str)
            if not ppd:
                plaintext_list.append(["FAILED", "", cipher_str])
            else:
                plaintext_list.extend(ppd)

    return plaintext_list


def main():
    # Take user input (file or string)
    inp_list = []
    if args.string:
        inp_list.append(args.input)
    elif args.file:  # Edit this pending input... currently reads line by line
        with open(args.input, 'r') as file:
            icl = file.readlines()
            for c in icl:
                inp_list.append(c[:-1])  # removes '\n'
    else:
        print("please specify -s or -f for a string or file input")
        print("Example usage: ./cryptool.py [input] -sd [cipher flag]")
        exit()

    # Encrypt or decrypt input
    # TODO issue here, what if put multiple flags for ciphers.  It would run them in this order...
    if args.decrypt:
        plaintext_list = []
        for arg in args.__dict__:
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key"]:
                if args.__dict__[arg]:
                    print_plaintext(given_cipher(arg, inp_list, key))
                    exit()

        # Otherwise, have to guess what cipher it is.
        print_plaintext(guess_cipher(inp_list))
        exit()

    elif args.encrypt:
        if args.file:
            print("File will be encrypted line by line.")
        opt = []

        gc = False
        for arg in args.__dict__:
            if arg not in ["input", "string", "file", "encrypt", "decrypt", "key"]:
                if args.__dict__[arg]:
                    for inp in inp_list:
                        opt.append(encrypt_cipher(arg, inp))
                    gc = True

        if gc is False:
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
