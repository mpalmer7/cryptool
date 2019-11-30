# Vigenère

lalpha = "abcdefghijklmnopqrstuvwxyz"
ualpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def code_char(char, key_char, type):
    if key_char in lalpha:
        kc = lalpha.index(key_char)  # .index finds first occurrence of item
    elif key_char in ualpha:
        kc = ualpha.index(key_char)
    else:
        return char

    if type == "d":
        if char in lalpha:
            return lalpha[((lalpha.index(char) - kc) % 26)]  # .index finds first occurrence of item
        elif char in ualpha:
            return ualpha[((ualpha.index(char) - kc) % 26)]
    elif type == "e":
        if char in lalpha:
            return lalpha[((lalpha.index(char) + kc) % 26)]  # .index finds first occurrence of item
        elif char in ualpha:
            return ualpha[((ualpha.index(char) + kc) % 26)]
    return char


def decrypt(inp_obj):
    key = inp_obj.key
    ctext = inp_obj.string

    if key is None:
        print("No key given, Vigenère cipher skipped.")
        return []
    org_key = key
    while len(key) <= len(ctext):
        key += org_key

    ptext = ""
    for i in range(len(ctext)):
        ptext += code_char(ctext[i], key[i], "d")

    # print(ptext)
    yield ptext


def encrypt(inp_obj):
    key = inp_obj.key
    inp = inp_obj.string

    if key is None:
        key = input("Please enter key string to encrypt with: ")
    org_key = key
    while len(key) <= len(inp):
        key += org_key

    ctext = ""
    for i in range(len(inp)):
        ctext += code_char(inp[i], key[i], "e")

    # print(ctext)
    return ctext
