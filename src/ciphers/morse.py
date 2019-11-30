mdict = {'-': 'T', '-.--': 'Y', '.': 'E', '-.-': 'K', '..---': '2',
         '.--': 'W', '-.': 'N', '.--.': 'P', '.-.': 'R', '...': 'S',
         '.---': 'J', '-..-': 'X', '...--': '3', '...-': 'V', '-....':
             '6', '--..': 'Z', '---': 'O', '-.-.': 'C', '-..': 'D', '----.':
             '9', '--.': 'G', '..-': 'U', '---..': '8', '-...': 'B', '..':
             'I', '.-..': 'L', '....-': '4', '..-.': 'F', '....': 'H', '.-':
             'A', '--': 'M', '--...': '7', '.....': '5', '--.-': 'Q', '-----':
             '0', '.----': '1'}


def decrypt(inp_obj):
    plaintext = ''
    for letter in inp_obj.string.split(' '):
        plaintext += str(mdict.get(letter))  # if letter not in mdict, adds "None"
    yield plaintext.replace("None", " ").lower()


def encrypt(inp_obj):
    ciphertext = ''
    for letter in list(inp_obj.string):
        for m, t in mdict.items():
            if t == letter.upper():
                ciphertext += m
                ciphertext += " "

    return ciphertext[:-1]  # gets rid of last space
