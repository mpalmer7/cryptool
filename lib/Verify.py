import cryptanalyzer

# sow3-6 is the official list of scrabble words, 3-6 letters in length
f = open("sow3-6.txt", "r")
sowpods = f.readlines()
for d in range(len(sowpods)):
    temp = (sowpods[d].strip("\n")).lower()
    sowpods[d] = temp
f.close()


def verify_cipher(p_p):
    cipher_weights = cryptanalyzer.cryptanalysis(p_p)[1]
    potential_ciphers = []
    for w in cipher_weights:
        if w in ["caesar", "atbash", "simplesub", "reversetext", "vigenere"]:
            pass
        else:
            if int(cipher_weights[w]) >= 7:  # arbitrary	#############################
                print("Potentially found a cipher within the cipher.")
                # print(p_p, w)
                potential_ciphers.append(w)
    return potential_ciphers


def verify_english(p_p):
    lp_counter = 0  # likely plaintext counter
    need_check_big = False
    # split p_p into words and remove all non-alphabetic characters
    working_text = p_p.split(' ')
    for n in range(len(working_text)):
        working_text[n] = ''.join([i for i in working_text[n] if i.isalpha()])
    # print(working_text)

    # if words are not separated by spaces
    if len(working_text) == 1:
        for word in sowpods:
            if word in working_text[0]:
                lp_counter += 1
    # we have separate words
    else:
        for test_word in sowpods:
            for p_p_word in working_text:
                if test_word == p_p_word.lower():
                    lp_counter += 1

        # this is separated to reduce time, long list of words
        for w in working_text:
            if len(w) > 6:
                need_check_big = True
        if need_check_big:
            # print("checking big words")
            try:
                f = open("sow7+.txt", "r")
                blw = f.readlines()  # big letter words
                for d in range(len(blw)):
                    temp = (blw[d].strip("\n")).lower()
                    blw[d] = temp
                f.close

                for test_word in blw:
                    for p_p_word in working_text:
                        if test_word == p_p_word.lower():
                            lp_counter += 1
            except FileNotFoundError:
                print("ERROR in VerifyPlaintext: Could not locate big words file, ignoring it...")
                pass

    is_word = lp_counter - (len(p_p) / 25)
    # print(p_p, is_word)

    return is_word


def verify_all(inp_list):
    ppd = {}  # potential plaintext dict

    # check against english
    for p_p in inp_list:  # potential plaintext
        is_word = verify_english(p_p)
        if is_word > 1:  # arbitrary...	########################################
            ppd[p_p] = is_word
        else:
            cipher_in_cipher = verify_cipher(p_p)
            if not cipher_in_cipher:
                pass
            else:
                ppd[p_p] = 0

    return sorted(ppd, key=ppd.get, reverse=True)
