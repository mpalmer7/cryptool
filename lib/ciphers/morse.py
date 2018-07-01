# Mitchell Palmer
# Updated: 7/1/18


def decrypt(ciphertext, nope=None):
    plaintext = ''
    mdict = {'-': 'T', '-.--': 'Y', '.': 'E', '-.-': 'K', '..---': '2',
             '.--': 'W', '-.': 'N', '.--.': 'P', '.-.': 'R', '...': 'S',
             '.---': 'J', '-..-': 'X', '...--': '3', '...-': 'V', '-....':
                 '6', '--..': 'Z', '---': 'O', '-.-.': 'C', '-..': 'D', '----.':
                 '9', '--.': 'G', '..-': 'U', '---..': '8', '-...': 'B', '..':
                 'I', '.-..': 'L', '....-': '4', '..-.': 'F', '....': 'H', '.-':
                 'A', '--': 'M', '--...': '7', '.....': '5', '--.-': 'Q', '-----':
                 '0', '.----': '1'}
    for letter in ciphertext.split(' '):
        plaintext += str(mdict.get(letter))  # if letter not in mdict, adds "None"
    return [plaintext.replace("None", " ").lower()]
