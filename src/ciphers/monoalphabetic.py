# WORK IN PROGRESS

import operator
import string, re

'''
Substitution cipher
Like caesar except no rotation
Pick randomly which letters to substitute
    a->z    b->c

Breaking substitution
can’t brute force
frequency analysis
quipqiup
https://quipqiup.com/

Additional reference:
http://practicalcryptography.com/ciphers/simple-substitution-cipher/
'''
alphabet = "abcdefghijklmnopqrstuvwxyz"

MUST_be_of = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [],
              'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],
              'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
CANT_be_of = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [],
              'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],
              'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}

def calc_inp_letter_frequency(ctext):
    inp_letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0,
                        'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0,
                        's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    characters_in_ctext = list(ctext.lower())  # ToDo all lowercase for now
    totalalphachars = 0
    for ch in characters_in_ctext:
        if ch.lower() in alphabet:
            inp_letter_count[ch.lower()] += 1
            totalalphachars += 1

    if totalalphachars == 0:
        return []

    # sorted frequency in ctext
    inp_letter_frequency = {}
    for lett in inp_letter_count:
        inp_letter_frequency[lett] = (inp_letter_count[lett] / totalalphachars) * 100
    sfic = sorted(inp_letter_frequency.items(), key=operator.itemgetter(1))[::-1]
    return sfic


def calc_inp_double_letters(ctext):
    bigram_dict = {}
    for c in range(len(ctext)-1):
        if ctext[c] == ctext[c+1]:
            if ctext[c] in bigram_dict:
                bigram_dict[ctext[c]] += 1
            else:
                bigram_dict[ctext[c]] = 1

    return sorted(bigram_dict.items(), key=operator.itemgetter(1))[::-1]


def calc_bigram_freq(ctext):
    bigram_dict = {}
    for c in range(len(ctext)-1):
        bigram = ctext[c:c+2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1

    to_pop = []
    for bigram in bigram_dict:
        if bigram_dict[bigram] <= 2:
            to_pop.append(bigram)
    for bigram in to_pop:
        bigram_dict.pop(bigram)

    return sorted(bigram_dict.items(), key=operator.itemgetter(1))[::-1]


def calc_trigram_freq(ctext):
    trigram_dict = {}
    for c in range(len(ctext)-2):
        trigram = ctext[c:c+3]
        if trigram in trigram_dict:
            trigram_dict[trigram] += 1
        else:
            trigram_dict[trigram] = 1

    to_pop = []
    for trigram in trigram_dict:
        if trigram_dict[trigram] <= 2:
            to_pop.append(trigram)
    for trigram in to_pop:
        trigram_dict.pop(trigram)

    return sorted(trigram_dict.items(), key=operator.itemgetter(1))[::-1]


class CipherText:
    def __init__(self, inp_str):
        self.ctext = inp_str
        self.certain_mappings = {}  # format 'a': 'o', means 'a' in ciphertext -> 'o' in plaintext
        self.possible_mappings = {'a': alphabet, 'b': alphabet, 'c': alphabet, 'd': alphabet,
                                  'e': alphabet, 'f': alphabet, 'g': alphabet, 'h': alphabet,
                                  'i': alphabet, 'j': alphabet, 'k': alphabet, 'l': alphabet,
                                  'm': alphabet, 'n': alphabet, 'o': alphabet, 'p': alphabet,
                                  'q': alphabet, 'r': alphabet, 's': alphabet, 't': alphabet,
                                  'u': alphabet, 'v': alphabet, 'w': alphabet, 'x': alphabet,
                                  'y': alphabet, 'z': alphabet}
        self.letter_frequency = calc_inp_letter_frequency(inp_str)
        self.double_letter_count = calc_inp_double_letters(inp_str)
        self.bigram_frequency = calc_bigram_freq(inp_str)
        self.trigram_frequency = calc_trigram_freq(inp_str)

    def add_certain_mapping(self, cipher_letter, plaintext_letter):
        # Add certain mapping
        self.certain_mappings[cipher_letter] = plaintext_letter
        del self.possible_mappings[cipher_letter]

        # Remove plaintext_letter from possible_mappings of other letters
        for letter in self.possible_mappings:
            self.possible_mappings[letter] = self.possible_mappings[letter].replace(plaintext_letter, '')

    def remove_possible_mapping(self, letter_list, impossible_letter):
        for letter in letter_list:
            self.possible_mappings[letter] = self.possible_mappings[letter].replace(impossible_letter, '')

    def check_only_one_mapping_for_cipherletter(self):
        for letter in self.possible_mappings:
            if len(self.possible_mappings[letter]) == 1:
                self.add_certain_mapping(letter, self.possible_mappings[letter])

    def check_only_one_mapping_for_plaintextletter(self):
        for p_letter in list(alphabet):
            n = 0
            cipher_letter = ''
            for c_letter in self.possible_mappings:
                if p_letter in self.possible_mappings[c_letter]:
                    n += 1
                    cipher_letter = c_letter
            if n == 1:
                self.add_certain_mapping(cipher_letter, p_letter)

    def print_analysis(self):
        print("Ciphertext:")
        print(self.ctext)
        print("\nHere is the analysis...\n")

        print("Letter frequency:")
        for x in self.letter_frequency:
            print(x[0] + ": " + str(x[1]))
        print("Double letter count:")
        for x in self.double_letter_count:
            print(x[0] + ": " + str(x[1]))
        print("Bigram count:")
        for x in self.bigram_frequency:
            print(x[0] + ": " + str(x[1]))
        print("Trigram count:")
        for x in self.trigram_frequency:
            print(x[0] + ": " + str(x[1]))


"""
def get_single_letter_frequency_match(opt_lst, ctext, sfic):
    english_frequency = {'e': 12.02, 't': 9.1, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
                         'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71,
                         'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11,
                         'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.1, 'z': 0.07}
    n = 0
    for char in english_frequency:
        opt_lst = replace_letter(opt_lst, ctext, sfic[n][0], char)
        n+= 1
    return opt_lst
"""


def decrypt(ctext, key=None):
    # print("".join(get_single_letter_frequency_match(opt_lst, ctext, sfic)))
    print("Analyzing ciphertext...")
    ctext_obj = CipherText(ctext)
    print("Done.")
    ctext_obj.print_analysis()


    """
    # via: http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    # based on sample of 40,000
    # assume error of += 0.01%
    # english_frequency = {'e': 12.02, 't': 9.1, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
    #                     'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71,
    #                     'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11,
    #                     'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.1, 'z': 0.07}

    # find words
    # ToDo what if no spaces????
    fwl = ctext.lower().split(" ")  # ToDo all lowercase for now
    words = {}
    for w in fwl:
        if w in words.keys():
            words[w] += 1
        else:
            words[w] = 1
    # print(words)

    ''' STEP 1 '''
    # replace most common letter with 'e'
    opt_lst = replace_letter(opt_lst, ctext, sfic[0][0], 'e') #ToDo temp, do at end
    update_must_cant(sfic[0][0], 'e')


    ''' STEP 2 '''
    # one letter words must be either 'I' or 'A'
    one_lw = {}
    for w in words:
        if len(w) == 1:
            one_lw[w] = words[w]
    # print(one_lw)

    # DOUBLE LETTERS, like 'aa' will never appear together.

    '''
    # find first letter frequency
    flf = {}
    for w in words:
        print(w)
        if w[0] in flf.keys():
            flf[w[0]] += words[w]
        else:
            flf[w[0]] = words[w]
    print(sorted(flf.items(), key=operator.itemgetter(1))[::-1])
    '''

    print("MUST")
    print(MUST_be_of)
    print("CANT")
    print(CANT_be_of)

    opt_str = ''.join(opt_lst)
    print(opt_str)
    pass
    """

decrypt(hw2_ciphertext)


def encrypt(plaintext, key=None):
    print("Simple Substitution encryption not implemented yet.")
    return None
