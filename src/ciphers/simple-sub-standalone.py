from math import log
import re

INPUT2 = "7 12 26 20   14 4   22 4 15   14 4   7 12 3 2   22 4 15   12 26 16 3   2 15 6 3 24 25 5   5 4 14 3 23   24 26 20 12 3 24   20 12 26 2   26 8 9 12 26 18 3 20 25 5   26 2 23 7 3 24    20 12 3   23 26 6 3   20 12 25 2 10    23 25 6 9 8 3   23 15 18 23 20 26 20 25 4 2 23   24 3 9 8 26 5 3   4 2 3   23 22 6 18 4 8   4 21   9 8 26 25 2 20 3 17 20   7 25 20 12   4 2 3   23 22 6 18 4 8   4 21   5 25 9 12 3 24 20 3 17 20"
INPUT3 = "Zpv lopx uif svmft boe tp ep J B gvmm dpnnjunfou't xibu J'n uijoljoh pg Zpv xpvmeo'u hfu uijt gspn boz puifs hvz J kvtu xboob ufmm zpv ipx J'n gffmjoh Hpuub nblf zpv voefstuboe Ofwfs hpoob hjwf zpv vq Ofwfs hpoob mfu zpv epxo Ofwfs hpoob svo bspvoe boe eftfsu zpv Ofwfs hpoob nblf zpv dsz Ofwfs hpoob tbz hppeczf Ofwfs hpoob ufmm b mjf boe ivsu zpv Xf'wf lopxo fbdi puifs gps tp mpoh Zpvs ifbsu't cffo bdijoh cvu Zpv'sf upp tiz up tbz ju Jotjef xf cpui lopx xibu't cffo hpjoh po Xf lopx uif hbnf boe xf'sf hpoob qmbz ju Boe jg zpv btl nf ipx J'n gffmjoh".lower()

with open("2600-0.txt", encoding="utf-8") as f:
    data = f.read()

INPUT = " ".join([re.sub(r"[^a-zA-Z]+", ' ', k.lower()) for k in data.split("\n")])
#print(INPUT)

# a block of text SHOULD work with WORD_DELIM = something that doesn't occur, and char delimeter = ""
CHAR_DELIMITER = ""
WORD_DELIMITER = " "

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ENGLISH_CHAR_FREQUENCY = {'e': 12.02, 't': 9.1, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
                         'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71,
                         'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,'v': 1.11,
                         'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.1, 'z': 0.07} # ToDo anything that grabs v, make it so it could also be k-z?
ENGLISH_BIGRAM_FREQUENCY = {'th': 2.71, 'en': 1.13, 'ng': 0.89, 'he': 2.33, 'at': 1.12, 'al': 0.88,
                            'in': 2.03, 'ed': 1.08, 'it': 0.88, 'er': 1.78, 'nd': 1.07, 'as': 0.87,
                            'an': 1.61, 'to': 1.07, 'is': 0.86, 're': 1.41, 'or': 1.06, 'ha': 0.83,
                            'es': 1.32, 'ea': 1.00, 'et': 0.76, 'on': 1.32, 'ti': 0.99, 'se': 0.73,
                            'st': 1.25, 'ar': 0.98, 'ou': 0.72, 'nt': 1.17, 'te': 0.98, 'of': 0.71}
ENGLISH_TRIGRAM_FREQUENCY = {'THE':1.81, 'ERE':0.31, 'HES':0.24, 'AND':0.73, 'TIO':0.31, 'VER':0.24,
                             'ING':0.72, 'TER':0.30, 'HIS':0.24, 'ENT':0.42, 'EST':0.28, 'OFT':0.22,
                             'ION':0.42, 'ERS':0.28, 'ITH':0.21, 'HER':0.36, 'ATI':0.26, 'FTH':0.21,
                             'FOR':0.34, 'HAT':0.26, 'STH':0.21, 'THA':0.33, 'ATE':0.25, 'OTH':0.21,
                             'NTH':0.33, 'ALL':0.25, 'RES':0.21, 'INT':0.32, 'ETH':0.24, 'ONT':0.20}
COMMON_TWO_LETTER_WORDS = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am']
COMMON_THREE_LETTER_WORDS = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was',
                             'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old',
                             'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']

# ToDo min value that only occurs once-twice; ignore and add all to possible lists?

# might be better to squish the scales of both using log... # TODO by squishing both, closer to gether max/min == better results
# https://en.wikipedia.org/wiki/Likelihood_function#Log-likelihood
# get ratios of logs instead of ratios
SINGLE_CHAR_JITTER = 0.3 # TODO modify jitter value based on total length of input
BIGRAM_JITTER = 1


def analyze_letter_frequency(cipher):
    for c_let in cipher.possible_mappings:
        still_possible = []
        for p_let in ENGLISH_CHAR_FREQUENCY:
            c_let_freq = float(cipher.letter_frequency[c_let])
            p_let_freq = ENGLISH_CHAR_FREQUENCY[p_let]
            if c_let_freq == 0.000:
                c_let_freq = 0.001
            if abs(log(p_let_freq) - log(c_let_freq)) <= SINGLE_CHAR_JITTER:
                still_possible.append(p_let)

        new_mapping = []
        for pos_map in cipher.possible_mappings[c_let]:
            if pos_map in still_possible:
                new_mapping.append(pos_map)

        cipher.possible_mappings[c_let] = new_mapping


def analyze_common_two_letters(cipher):
    for word in cipher.words:
        if len(word) == 2:
            first_letter = word[0]
            second_letter = word[1]

            first_letter_probable_options = list(set([x[0] for x in COMMON_TWO_LETTER_WORDS]))
            second_letter_probable_options = list(set([x[1] for x in COMMON_TWO_LETTER_WORDS]))

            new_2_mapping = []
            for let in cipher.possible_mappings[first_letter]:
                if let in first_letter_probable_options:
                    new_2_mapping.append(let)
            if new_2_mapping:
                cipher.possible_mappings[first_letter] = new_2_mapping
            # else - dont update it

            new_2_mapping = []
            for let in cipher.possible_mappings[second_letter]:
                if let in second_letter_probable_options:
                    new_2_mapping.append(let)
            if new_2_mapping:
                cipher.possible_mappings[second_letter] = new_2_mapping
            # else - dont update it


def analyze_bigram_frequency(cipher):
    still_possible = {}
    for c_bigram in cipher.bigram_frequency:
        for p_bigram in ENGLISH_BIGRAM_FREQUENCY:
            c_bigram_freq = float(cipher.bigram_frequency[c_bigram])
            p_bigram_freq = ENGLISH_BIGRAM_FREQUENCY[p_bigram]

            if abs(log(p_bigram_freq) - log(c_bigram_freq)) <= BIGRAM_JITTER:
                if c_bigram[0] in still_possible:
                    still_possible[c_bigram[0]].append(p_bigram[0])
                else:
                    still_possible[c_bigram[0]] = [p_bigram[0]]

                if c_bigram[1] in still_possible:
                    still_possible[c_bigram[1]].append(p_bigram[1])
                else:
                    still_possible[c_bigram[1]] = [p_bigram[1]]

        for key in still_possible:
            still_possible[key] = list(set(still_possible[key]))
        #print(still_possible)

        for c_let in cipher.possible_mappings:
            new_mapping = []
            for pos_map in cipher.possible_mappings[c_let]:
                try:
                    if pos_map in still_possible[c_let]:
                        new_mapping.append(pos_map)
                except KeyError:
                    new_mapping.append(pos_map)

            cipher.possible_mappings[c_let] = new_mapping


def calc_dict_freq(count_dict):
    freq_dict = {}

    total_count = sum([count_dict[x] for x in count_dict])

    for x in count_dict:
        freq_dict[x] = str((count_dict[x] / total_count) * 100)[:5]

    return freq_dict


class Cipher:
    def __init__(self):
        self.full = INPUT  # str
        self.words = INPUT.split(WORD_DELIMITER)  # list

        self.letter_frequency = self._get_letter_frequency()

        self.bigram_frequency = self._get_bigram_frequency()
        self.trigram_frequency = self._get_trigram_frequency()

        self.possible_mappings = self._set_possible_mappings()
        self.certain_mappings = self._set_certain_mappings()

    def _get_letter_frequency(self):
        letter_occurrences = {}
        for word in self.words:
            if CHAR_DELIMITER:
                chars = word.split(CHAR_DELIMITER)
            else:
                chars = list(word)
            for c in chars:
                if c != '':
                    if c in letter_occurrences:
                        letter_occurrences[c] += 1
                    else:
                        letter_occurrences[c] = 1

        letter_frequency = calc_dict_freq(letter_occurrences)

        return letter_frequency

    def _get_bigram_frequency(self):
        bigrams = {}
        for word in self.words:
            if CHAR_DELIMITER:
                chars = word.split(CHAR_DELIMITER)
            else:
                chars = list(word)
            for c in range(len(chars) - 1):  # -1: we dont need end letter since checking for double
                bigram = chars[c] + CHAR_DELIMITER + chars[c+1]
                if bigram in bigrams:
                    bigrams[bigram] += 1
                else:
                    bigrams[bigram] = 1

        bigram_frequency = calc_dict_freq(bigrams)

        return bigram_frequency

    def _get_trigram_frequency(self):
        trigrams = {}
        for word in self.words:
            if CHAR_DELIMITER:
                chars = word.split(CHAR_DELIMITER)
            else:
                chars = list(word)
            for c in range(len(chars) - 2):  # -2: we dont need end letters since checking for triple
                trigram = chars[c] + CHAR_DELIMITER + chars[c+1] + CHAR_DELIMITER + chars[c+2]
                if trigram in trigrams:
                    trigrams[trigram] += 1
                else:
                    trigrams[trigram]  = 1

        trigram_frequency = calc_dict_freq(trigrams)

        return trigram_frequency

    def _set_possible_mappings(self):
        possible_mappings = {}
        for letter in self.letter_frequency:
            # ignoring frequency for now, I just want to know all the letters used...
            possible_mappings[letter] = list(ALPHABET)
        return possible_mappings

    def _set_certain_mappings(self):
        certain_mappings = {}
        for letter in self.letter_frequency:
            # ignoring frequency for now, I just want to know all the letters used...
            certain_mappings[letter] = []
        return certain_mappings

    def update_certain(self):
        # update certain
        for letter in self.possible_mappings:
            if len(self.possible_mappings[letter]) == 1:
                self.certain_mappings[letter] = self.possible_mappings[letter][0]

                # remove from possible
                for l2 in self.possible_mappings:
                    if self.possible_mappings[letter][0] in self.possible_mappings[l2] and l2 != letter:
                        new_mapping = []
                        for p2 in self.possible_mappings[l2]:
                            if p2 != self.possible_mappings[letter][0]:
                                new_mapping.append(p2)
                        self.possible_mappings[l2] = new_mapping



def main():
    cipher = Cipher()

    print("Letter Frequency: {}".format({k: v for k, v in sorted(cipher.letter_frequency.items(), key=lambda item: item[1])}))
    print("Bigrams: {}".format({k: v for k, v in sorted(cipher.bigram_frequency.items(), key=lambda item: item[1])}))
    print("Trigrams: {}".format({k: v for k, v in sorted(cipher.trigram_frequency.items(), key=lambda item: item[1])}))

    analyze_letter_frequency(cipher)
    #analyze_bigram_frequency(cipher) # todo still an error here
    # todo add certain letters


    # ToDo - hardcoded for first problem
    #cipher.possible_mappings["10"] = list(ALPHABET)
    #cipher.possible_mappings["16"] = list(ALPHABET)

    cipher.update_certain()

    # analyze_common_two_letters(cipher) # ToDo broken

    print(cipher.possible_mappings.keys())
    
    for letter in cipher.possible_mappings:
        print(letter + ": " + str(cipher.possible_mappings[letter]))

    #for word in INPUT.split(" "):
    #    if CHAR_DELIMITER:
    #        chars = word.split(CHAR_DELIMITER)
    #    else:
    #        chars = list(word)
    #    for c in chars:
    #        if c and len(cipher.possible_mappings[c]) == 1 and cipher.possible_mappings[c][0] != 'k':
    #            print(cipher.possible_mappings[c][0] + " ", end='')
    #        else:
    #            print('-' + " ", end='')
    #    print("   ", end='')


if __name__ == "__main__":
    main()