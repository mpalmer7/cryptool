import cryptanalyzer

# sow3-6 is the official list of scrabble words, 3-6 letters in length
f = open("sow3-6.txt", "r")
sowpods = f.readlines()
for d in range(len(sowpods)):
    temp = (sowpods[d].strip("\n")).lower()
    sowpods[d] = temp
f.close()
# 7+ letter words is a much larger set than 3-6 so I split it to use this less
f = open("sow7+.txt", "r")
blw = f.readlines()  # big letter words
for d in range(len(blw)):
    temp = (blw[d].strip("\n")).lower()
    blw[d] = temp
f.close


def verify_cipher(p_p):
    cipher_weights = cryptanalyzer.cryptanalysis(p_p)[1]
    potential_ciphers = {}
    for w in cipher_weights:
        if w in ["caesar", "atbash", "simplesub", "reversetext", "vigenere"]:
            pass  # too easily mistaken with English; therefore skip
        else:
            if int(cipher_weights[w]) >= 7:  # TODO arbitrary ceiling...
                print("Potentially found a cipher within the cipher.")
                # print(p_p, w)
                potential_ciphers[w] = cipher_weights[w]
    counter = 0
    likely_cipher = ""
    for pc in potential_ciphers:
        if potential_ciphers[pc] > counter:
            counter = potential_ciphers[pc]
            likely_cipher = pc

    return likely_cipher


def verify_english(p_p):
    words_found = 0
    working_text = p_p.split(' ')
    # file of six letter words is separated to reduce time; giant list
    need_check_big = False
    for w in working_text:
        if len(w) > 6:
            need_check_big = True

    # split p_p into words and remove all non-alphabetic characters
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
        # check 6+ letter words; if needed
        if need_check_big:
            for test_word in blw:
                for p_p_word in working_text:
                    if test_word == p_p_word.lower():
                        words_found += 1

    # TODO arbitrary; if the amount of words found is greater than 1/25 of the total phrase, probably English
    if words_found - (len(p_p) / 25) > 1:
        return True
    else:
        return False


def verify_all(inp_list):
    inv = []  # input now verified
    for p_p in inp_list:  # potential_plaintext
        if verify_english(p_p):  # check against english
            inv.append([p_p, "English"])
        else:
            cipher_in_cipher = verify_cipher(p_p)
            if not cipher_in_cipher:
                pass
            else:
                inv.append([p_p, cipher_in_cipher])
    return inv
