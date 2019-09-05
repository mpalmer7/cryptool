# need training data...
# tensorflow (from google) library for machine learning
# cykit learn

L_ALPHA = "abcdefghijklmnopqrstuvwxyz"
U_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMERICALS = "1234567890"
SYMBOLS = "!@#$%^&*()_+" + "`~{[}]_-+=|\\\"':;?/>.<,"
SPACE = " "


def get_chars(inp_cipher):
    cod = {}
    for char in inp_cipher.ctext:
        if char in cod.keys():
            cod[char] += 1
        else:
            cod[char] = 1
    # change to percentage based
    for c in cod:
        cod[c] = cod[c] / inp_cipher.total_number_of_chars
    return cod  # character occurrence dictionary


def get_sets(inp_cipher):
    sod = {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 0, SYMBOLS: 0, SPACE: 0}
    for char in inp_cipher.ctext:
        for s in sod:
            if char in s:
                sod[s] += 1
                break
    # change to percentage based
    for s in sod:
        sod[s] = sod[s] / inp_cipher.total_number_of_chars
    return sod


def get_words(inp_cipher, delimeter=" "):  # ToDo add option to pass delimiter
    word_list = inp_cipher.ctext.split(delimeter)
    if len(word_list) > 1:
        return True
    else:
        return False


class Cipher:
    def __init__(self, type, param_1):
        if type == "base":
            self.name = param_1["name"] # str, cipher name

            self.cod = param_1["cod"]  # dic, character occurrence percentage
            self.sod = param_1["sod"]  # dic, set occurrence percentage
            self.word_boo = param_1["words"]  # boo, are there multiple words
        elif type == "input":
            self.ctext = param_1
            self.total_number_of_chars = len(param_1)

            self.cod = get_chars(self)
            self.sod = get_sets(self)
            self.word_boo = get_words(self)

    def compare_cod(self, cipher_2):
        score = 0
        for char in self.cod:
            if char in cipher_2.cod.keys():
                score += cipher_2.cod[char] * self.cod[char]
            else:
                score += cipher_2.cod["OTHER"] * self.cod[char]
        return score

    def compare_sod(self, cipher_2):
        score = 0
        for s in self.sod:
            score += cipher_2.sod[s] * self.sod[s]
        return score

    def analyse_b64_closeness(self):
        # b64 will add '=' to make it divisible by 4
        if ((self.total_number_of_chars % 4) == 0) or \
           ((self.total_number_of_chars - 3) % 4 == 0):
            if "=" in self.ctext[-4:-1]:
                return 20
            return 8
        return -5


# ToDo create dir for cipher jsons, then refactor this to open those files in a for loop, make it easier to add a cipher
BINARY_CIPHER = Cipher("base", {"name": "binary",
                                "cod": {"1": 10, "0": 10, " ": 5, "OTHER": 0},
                                "sod": {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 10, SYMBOLS: 0, SPACE: 5},
                                "words": {True: 5, False: 5}})
BASE64_CIPHER = Cipher("base", {"name": "base64",
                                "cod": {"OTHER": 5},
                                "sod": {L_ALPHA: 5, U_ALPHA: 5, NUMERICALS: 5, SYMBOLS: 4, SPACE: -5},
                                "words": {True: -5, False: 10}})
MORSE_CIPHER = Cipher("base", {"name": "morse",
                               "cod": {".": 10, "-": 10, " ": 5, "OTHER": 0},
                               "sod": {L_ALPHA: 0, U_ALPHA: 0, NUMERICALS: 0, SYMBOLS: 10, SPACE: 5},
                               "words": {True: 5, False: 3}})
SINGLEBYTEXOR_CIPHER = Cipher("base", {"name": "singlebyteXOR",
                                       "cod": {"OTHER": 5},
                                       "sod": {L_ALPHA: 5, U_ALPHA: 5, NUMERICALS: 5, SYMBOLS: 0, SPACE: 0},
                                       "words": {True: 0, False: 10}})
SUBTYPECIPHERS_CIPHER = Cipher("base", {"name": "subtypeciphers",
                                        "cod": {"-": 2, "1": 0, "0": 0, "OTHER": 5},
                                        "sod": {L_ALPHA: 10, U_ALPHA: 10, NUMERICALS: 0, SYMBOLS: 0, SPACE: 5},
                                        "words": {True: 8, False: 3}})
MODERN_CIPHER = Cipher("base", {"name": "modern",
                                    "cod": {"OTHER": 5},
                                    "sod": {L_ALPHA: 5, U_ALPHA: 2, NUMERICALS: 5, SYMBOLS: 0, SPACE: -5},
                                    "words": {True: -10, False: 10}})
CIPHER_LIST = [BINARY_CIPHER, BASE64_CIPHER, MORSE_CIPHER, SINGLEBYTEXOR_CIPHER,
               SUBTYPECIPHERS_CIPHER, MODERN_CIPHER]


def cryptanalysis(ciphertext):  # string
    inp_cipher = Cipher("input", ciphertext)

    # Reinforcement machine learning?
    # if it gets the correct code add +.01 to the value, otherwise -.01 (or something along those lines...)
    weights = {}
    for base_cipher in CIPHER_LIST:
        score = 5
        # Returns closeness score for cod between inp and base, average this with current score
        score = (score + inp_cipher.compare_cod(base_cipher)) / 2
        # Returns closeness score for sod between inp and base, average this with current score
        score = (score + inp_cipher.compare_sod(base_cipher)) / 2

        # Update score with value of if there is words or if one long string
        # This is weighted at 1/3 affective rather than 1/2
        if inp_cipher.word_boo:
            score = (score*2 + base_cipher.word_boo[True]) / 3
        else:
            score = (score*2 + base_cipher.word_boo[False]) / 3

        # additional indicators: b64
        if base_cipher.name == "base64":
            score = (score + inp_cipher.analyse_b64_closeness()) / 2
        else:
            score = (score + abs(inp_cipher.analyse_b64_closeness())) / 2

        # additional indicators: singlebyteXOR
        if inp_cipher.ctext[0:2] == "1b":
            if base_cipher.name == "singlebyteXOR" or base_cipher.name == "base64":
                score = (score + 20) / 2
            else:
                score = (score + 0) / 2
        else:
            if base_cipher.name == "singlebyteXOR":
                score = (score - 5) / 2

        # additional indicators: modern
        if base_cipher.name == "modern":
            if inp_cipher.total_number_of_chars % 8 == 0:
                score = (score + 8) / 2
            else:
                score = (score - 5) / 2


        # subtypeciphers includes caesar, atbash, monoalphabetic, reverse text, vigenere
        if base_cipher.name == "subtypeciphers":
            weights["atbash"] = score
            weights["caesar"] = score - 0.25
            weights["vigenere"] = score - 0.5
            weights["reversetext"] = score - 0.75
            weights["monoalphabetic"] = score - 1
        elif base_cipher.name == "modern":
            weights["hash"] = score
            weights["aes"] = score - 0.25
        else:
            weights[base_cipher.name] = score

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # print(ctext)
    # print(weights)
    # print(sorted(weights, key=weights.get, reverse=True))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    final_weights = {}
    for ciph in weights:
        if weights[ciph] > 4:   # arbitrary
            final_weights[ciph] = weights[ciph]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # print(inp_cipher.ctext)
    # print(final_weights)
    # print(sorted(final_weights, key=final_weights.get, reverse=True))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    return [sorted(final_weights, key=final_weights.get, reverse=True), final_weights]

# cryptanalysis(input("Enter code: "))
