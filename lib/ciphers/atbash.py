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

def bothcrypt(inp):
    opt = ''
    for letter in list(inp):
        if letter in udict.keys():
            opt += str(udict.get(letter))
        elif letter in ldict.keys():
            opt += str(ldict.get(letter))
        else:
            opt += letter
    return opt

def decrypt(ciphertext, nullthing=None):
    # decryption
    plaintext = bothcrypt(ciphertext)
    # output
    if plaintext == '':
        return []
    else:
        return [plaintext]


def encrypt(inp, key=None):
    return bothcrypt(inp)