# Vigenère

lalpha = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"


def code_char(char, key_char):
    if key_char in lalpha:
        kc = lalpha.index(key_char)  # .index finds first occurrence of item
    elif key_char in ualpha:
        kc = ualpha.index(key_char)
    else:
        return char

    if char in lalpha:
        return lalpha[lalpha.index(char) + lalpha.index(char) - kc]  # .index finds first occurrence of item
    elif char in ualpha:
        return ualpha[ualpha.index(char) + ualpha.index(char) - kc]
    else:
        return char


def decrypt(ctext, key=None):
    if key is None:
        print("No key given, Vigenère cipher skipped.")
        return []
    org_key = key
    while len(key) <= len(ctext):
        key += org_key

    ptext = ""
    for i in range(len(ctext)):
        ptext += code_char(ctext[i], key[i])

    print(ptext)
    return [ptext]


def encrypt(inp):
    print("Vigenère encryption not implemented yet.")
    exit()
