# Mitchell Palmer
# Updated: 7/1/18

lalpha = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"


def check_keys(phrase, key):
    decoded = ""
    cipher_index = 0
    for i in range(len(phrase)):
        if phrase[i] in lalpha:
            decoded += lalpha[lalpha.index(phrase[i]) + key]  # .index finds first occurrence of item
        elif phrase[i] in ualpha:
            decoded += ualpha[ualpha.index(phrase[i]) + key]
        else:
            decoded += phrase[i]
    return decoded


def decrypt(inp, key=None):
    ctext = list(inp)
    if key is not None:
        return [check_keys(ctext, key)]
    else:  # Key not given, try all keys
        all_combos = []
        for key in range(0, 26):
            all_combos.append(check_keys(ctext, key))
            key += 1
        return all_combos


def encrypt(plaintext):
    key = int(input("Enter an integer (0-26) to rotate by: "))
    return check_keys(plaintext, key)

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
