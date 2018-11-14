import cryptanalyzer

# sow3-6 is a list of legitimate scrabble words, 3-6 letters in length
f = open("sow3-6.txt", "r")
sowpods = f.readlines()
for d in range(len(sowpods)):
    temp = (sowpods[d].strip("\n")).lower()
    sowpods[d] = temp
f.close()
# there are much more 7+ letter words - this file is larger - but they are used less often
# therefore, I split it up so this would run faster
f = open("sow7+.txt", "r")
blw = f.readlines()  # big letter words
for d in range(len(blw)):
    temp = (blw[d].strip("\n")).lower()
    blw[d] = temp
f.close()


def verify_cipher(p_p):
    cipher_weights = cryptanalyzer.cryptanalysis(p_p)[1]
    potential_ciphers = {}
    for w in cipher_weights:
        if w in ["caesar", "atbash", "simplesub", "reversetext", "vigenere"]:
            pass  # too easily mistaken with English; therefore skip
        else:
            if int(cipher_weights[w]) >= 6:  # TODO arbitrary ceiling...
                print("Potentially found a cipher within the cipher.")
                # print(p_p, w)
                potential_ciphers[w] = cipher_weights[w]
    counter = 0

    likely_cipher = None
    for pc in potential_ciphers:
        if potential_ciphers[pc] > counter:
            counter = potential_ciphers[pc]
            likely_cipher = pc

    return likely_cipher


def verify_english(p_p):
    words_found = 0
    # split p_p into words and remove all non-alphabetic characters
    working_text = p_p.split(' ')
    for n in range(len(working_text)):
        working_text[n] = ''.join([i for i in working_text[n] if i.isalpha()])

    # if words are not separated by spaces
    if len(working_text) == 1:
        for word in sowpods:
            if word in working_text[0]:
                words_found += 1
    # otherwise; we have separate words
    else:
        for test_word in sowpods:
            for p_p_word in working_text:
                if test_word == p_p_word.lower():
                    words_found += 1
        # file of 7+ letter words is separated to speed up program
        # if any word is 7 letters or larger, then check these words; otherwise don't
        for w in working_text:
            if len(w) > 6:
                for test_word in blw:
                    for p_p_word in working_text:
                        if test_word == p_p_word.lower():
                            words_found += 1
                break

    # TODO arbitrary; if the amount of words found is greater than 1/20 of the total phrase => probably English
    if words_found - (len(p_p) / 20) > 1:
        return True
    else:
        return False


def verify_all(inp_list, boo_cic=False):  # cic is optional check for ciphers within ciphers
    inv = []  # input now verified
    for p_p in inp_list:  # potential_plaintext
        # check against english dictionary
        if verify_english(p_p):
            inv.append([p_p, "English"])
        else:
            if boo_cic:
                # check against cipher dictionary
                cipher_in_cipher = verify_cipher(p_p)
                if cipher_in_cipher:
                    inv.append([p_p, cipher_in_cipher])
    return inv
