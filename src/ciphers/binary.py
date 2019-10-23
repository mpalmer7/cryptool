import re


def decrypt(ciphertext, key=None):
    """Converts a binary string to utf-8 decoded text. Can guess the delimiter, if used."""
    # Break by delimiter(s) by stripping all non 0's or 1's
    inp_lst = ['']
    n = 0
    for char in ciphertext:
        if char == '1' or char == '0':
            inp_lst[n] += char
        else:
            # inp_lst.append(char)
            inp_lst.append('')
            n += 1  # 2

    opt_str = ''

    # No delimiter
    if len(inp_lst) == 1:
        for n in range(4, 17):
            for byte in re.findall('.{1,%s}' % n, inp_lst[0]):
                if byte:
                    opt_str += chr(int(byte, 2))
            yield opt_str
            opt_str = ''
    # delimiter found
    else:
        for byte in inp_lst:
            if byte:
                opt_str += chr(int(byte, 2))
        yield opt_str


def encrypt(plaintext, key=None):
    """utf-8 decode a string and convert it to binary, return the string of 1's and 0's delimited by a ' '"""
    opt_str = ''
    for char in plaintext:
        opt_str += str(int(bin(ord(char))[2:])) + " "
    return opt_str


def bin_fix(inp):
    # Binary fix...
    new = inp.replace("B", "0")
    new = new.replace("A", "1")

    new2 = inp.replace("A", "0")
    new2 = new2.replace("B", "1")

    print(new)
    print(new2)