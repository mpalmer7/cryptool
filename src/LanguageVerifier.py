import os

import cryptanalyzer


# lang3 is 3-6 letter words, lang7 is 7+ letter words
# I broke it up this way for efficiency. 1-2 letter words aren't helpful in detection.
# If you can establish a connection without having to go into 7+ letter words it runs so much faster.
# Since most words *english at least* will be shorter than 7 letters in your average sentence, ignore them for now.
class Language:
    def __init__(self, lang_name):
        self.name = lang_name

        self.lang3 = []
        if os.path.isfile("languages\{}_3.txt".format(lang_name)):
            f = open("languages\{}_3.txt".format(lang_name), "r")
            words = f.readlines()
            for i in range(len(words)):
                self.lang3.append((words[i].strip("\n")).lower())
            f.close()

        self.lang7 = []
        if os.path.isfile("languages\{}_7.txt".format(lang_name)):
            f = open("languages\{}_7.txt".format(lang_name), "r")
            words = f.readlines()
            for i in range(len(words)):
                self.lang7.append((words[i].strip("\n")).lower())
            f.close()


# To add a new language, create two text files with the language's name in "languages" directory
# Have the first be called "<LANGUAGE>_3.txt" with every 3-6 letter word in the language, one per line.
# Do the same for 7, but these are 7+ letter words.
# ToDo this system is still a bit awkward
def compile_languages():
    for dirpath, dirnames, filenames in os.walk("languages"):

        for filename in filenames:
            if filename.endswith("_3.txt"):
                lang_name = filename.split("_3.txt")[0]
                if os.path.exists("languages/"+filename+"_7.txt"):
                    yield Language(lang_name)


# Run this if you know input is a word
# Verifies if the word exists in a given language
def verify_word(given_word, lang_obj):
    if len(given_word) < 7:
        for lang_word in lang_obj.lang3:
            if given_word.lower() == lang_word:
                return True
    else:  # word length is 7 or greater
        for lang_word in lang_obj.lang7:
            if given_word.lower() == lang_word:
                return True
    return False


# Run this if given an unknown string that may contain one word or many words
# Returns Boolean
# Todo Maybe change return to: Verifies if the string is *likely* made up of words in a given language, scale 1-10
def verify_string(given_string, lang_obj, phrase_delimeter=' '):
    # Try to split by word delimiter (default: spaces)
    if phrase_delimeter in given_string:
        # split plaintext into words and remove all non-alphabetic characters; convert all characters to lowercase
        given_wordlist = given_string.split(' ')
        for n in range(len(given_wordlist)):
            given_wordlist[n] = ''.join([i.lower() for i in given_wordlist[n] if i.isalpha()])
        
        words_matched = 0
        for given_word in given_wordlist:
            if verify_word(given_word, lang_obj):
                words_matched += 1

        # Have certainty be percentage of words matched with words in the language
        certainty = (words_matched / len(given_wordlist))
        # Todo ARBITRARY analysis - If over 50% of words match, probably a good result
        if certainty > 0.5:
            return True

    # Not doing else statement for cases where a delimiter (e.g. space) is in a phrase but doesn't separate words
    # ...we want to still catch those
    words_matched = 0
    for word in lang_obj.lang3:
        if word in given_string.lower():
            words_matched += 1
    # TODO arbitrary; if the amount of words found is greater than 1/20 of the total phrase => probably English
    if (words_matched - (len(given_string) / 20)) > 1:
        return True
    # Still not there? Now tries 7+ letter word search
    for word in lang_obj.lang7:
        if word in given_string.lower():
            words_matched += 1
    if (words_matched - (len(given_string) / 20)) > 1:
        return True
    # Nope, the phrase is not of that language.
    return False


def verify_phrase_is_cipher(plaintext):
    cipher_weights = cryptanalyzer.cryptanalysis(plaintext)[1]
    potential_ciphers = {}
    for w in cipher_weights:
        if w in ["caesar", "atbash", "simplesub", "reversetext", "vigenere"]:
            pass  # too easily mistaken with English; therefore skip
        else:
            if int(cipher_weights[w]) >= 6:  # TODO arbitrary...
                print("Potentially found a cipher within the cipher.")
                # print(plaintext, w)
                potential_ciphers[w] = cipher_weights[w]

    counter = 0
    likely_cipher = None
    for pc in potential_ciphers:
        if potential_ciphers[pc] > counter:
            counter = potential_ciphers[pc]
            likely_cipher = pc

    return likely_cipher
