
lalpha = "abcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def check_keys(phrase, key):
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
    ctext = list(inp)
    if key is not None:
        yield check_keys(ctext, key)
    else:  # Key not given, try all keys
        for key in range(0, 26):
            yield check_keys(ctext, key)
            key += 1


def encrypt(plaintext, key=None):
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

"""
# run standalone
def Caesar():
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
"""
