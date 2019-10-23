
lalpha = "abcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def check_keys(phrase, key):
    """Helper function for decrypt(); takes input string and rotates its characters around the alphabet."""
    decoded = ""
    for i in range(len(phrase)):
        if phrase[i] in lalpha:
            decoded += lalpha[(lalpha.index(phrase[i]) - int(key)) % 26]  # .index finds first occurrence of item
        elif phrase[i] in ualpha:
            decoded += ualpha[(ualpha.index(phrase[i]) - int(key)) % 26]
        else:
            decoded += phrase[i]
    return decoded


def decrypt(inp, key=None):
    """Takes a string input, decrypts with the caesar cipher, and returns a string output.
    Will return all possible combinations if no key is given."""
    ctext = list(inp)
    if key is not None:
        yield check_keys(ctext, key)
    else:  # Key not given, try all keys
        for key in range(0, 26):
            yield check_keys(ctext, key)
            key += 1


def encrypt(plaintext, key=None):
    """Takes a string input, encrypts with the caesar cipher. If no key to rotate with is given,
    will prompt user to input the key they want to use."""
    if key is None:
        key = int(input("Enter an integer to rotate by: "))

    encoded = ""
    for i in range(len(plaintext)):
        if plaintext[i] in lalpha:
            encoded += lalpha[(lalpha.index(plaintext[i]) + int(key)) % 26]  # .index finds first occurrence of item
        elif plaintext[i] in ualpha:
            encoded += ualpha[(ualpha.index(plaintext[i]) + int(key)) % 26]
        else:
            encoded += plaintext[i]
    return encoded


def caesar():
    """This cipher can be run standalone. Encryption/decryption with the caesar cipher."""

    pt = input("Enter a phrase: ")
    huh = input("Encrypt (E) or Decrypt (D)? ")
    if (huh.lower() == "e") or ("encrypt" in huh.lower()):
        print("Encrypted Phrase: %s" % encrypt(pt))
    elif (huh.lower() == "d") or ("decrypt" in huh.lower()):
        key = input("Enter the decryption key (leave blank otherwise): ")
        if key != '':
            try:
                print("Decrypted Phrase: %s" % decrypt(pt, int(key)))
            except ValueError:
                print("Key not reconized... showing all options.")
                print("Decrypted Phrase: %s" % decrypt(pt))
        else:
            print("Decrypted Phrase: %s" % decrypt(pt))
    else:
        print("Input not reconized, exiting.")
        exit()
# Ceasar()