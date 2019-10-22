# Mitchell Palmer
# Updated: 7/1/18

udict = {'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T',
         'H': 'S', 'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N', 'N': 'M',
         'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I', 'S': 'H', 'T': 'G', 'U': 'F',
         'V': 'E', 'W': 'D', 'X': 'C', 'Y': 'B', 'Z': 'A'}
ldict = {'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v', 'f': 'u', 'g': 't',
         'h': 's', 'i': 'r', 'j': 'q', 'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm',
         'o': 'l', 'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g', 'u': 'f',
         'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b', 'z': 'a'}


def atb(inp_str):
    """Given a string as input, calculate the atbash cipher on it and return the result as a string."""
    opt = ''
    for letter in list(inp_str):
        if letter in udict.keys():
            opt += str(udict.get(letter))
        elif letter in ldict.keys():
            opt += str(ldict.get(letter))
        else:
            opt += letter
    if opt != '':
        return opt


def decrypt(ciphertext, nullthing=None):
    """Decrypts the atbash cipher, yields a string as the result."""
    yield atb(ciphertext)


def encrypt(inp, key=None):
    """Encrypts the atbash cipher, returns a string as the result."""
    return atb(inp)