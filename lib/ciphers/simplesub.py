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


# Test Case: giuifg cei iprc tpnn du cei qprcni
def update_potential_letters(pl, rm_char, other_than):  # pl is potential_letters, other_than is a list
    for ch in pl.keys():
        if ch not in other_than:
            pl[ch].remove(rm_char)
    return pl


def check_2_letter_words(pl):
    # 2 letter words
    # ox, ax, ex, by, my, up, um, of, if, me, ow, am, we, uh, be, oh, go, eh, ah, he,
    # hi, yo, us, on, in, an, do, no, as, at, it, is, or, so
    return pl


def decrypt(ctext, nullthing=None):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    numericals = "0123456789"
    symbols = " !@#$%^&*()-_+=\\|\"':;<>,.?/[]{}"
    characters_in_ctext = list(ctext)

    # print(ctext)
    # print(characters_in_ctext)

    if len(ctext) > 200:  # 200 arbitrary... #############

        # via: http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        # based on sample of 40,000
        # assume error of += 0.01%
        english_frequency = {'e': 12.02, 't': 9.1, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
                             'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71,
                             'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11,
                             'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.1, 'z': 0.07}

        inp_letter_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0,
                            'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0,
                            's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

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

        # sorted frequency in ctext
        sfic = sorted(inp_letter_frequency.items(), key=operator.itemgetter(1))[::-1]
        # print(sfic)

        opt_lst = list("_" * len(ctext))
        potential_letters = {
            'a': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'b': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'c': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'd': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'e': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'f': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'g': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'h': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'i': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'j': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'k': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'l': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'm': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'n': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'o': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'p': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'q': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'r': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            's': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            't': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'u': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'v': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'w': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'x': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'y': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z'],
            'z': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']}
        letters_it_has_to_be = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [],
                                'j': [], 'k': [], 'l': [], 'm': [], 'n': [],
                                'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [],
                                'x': [], 'y': [], 'z': []}

        # replace most common character with 'e'
        letters_it_has_to_be[sfic[0][0]].append('e')
        potential_letters[sfic[0][0]] = 'e'
        potential_letters = update_potential_letters(potential_letters, 'e', [sfic[0][0]])

        for ch in range(len(characters_in_ctext)):
            if characters_in_ctext[ch] == sfic[0][0]:
                opt_lst[ch] = 'e'

        # find a or i or both
        inp_split_by_space = ctext.split(" ")
        i_or_a = []
        for word in inp_split_by_space:
            if len(word) == 2:
                temp = list(word)
                if temp[0] in alphabet:
                    if temp[1] in alphabet:
                        pass
                    else:
                        i_or_a.append(temp[0])
                elif temp[1] in alphabet:
                    i_or_a.append(temp[0])
            elif len(word) == 1:
                if word in alphabet:
                    i_or_a.append(word)

        temp = set(i_or_a)
        i_or_a = []
        for t in temp:
            i_or_a.append(t)
        piplup = len(i_or_a)
        if piplup > 2:
            print("ERROR in simplesub: multiple single letter words detected (ln 91).")
            exit()
        elif piplup == 2:
            letters_it_has_to_be[i_or_a[0]].append('i')
            letters_it_has_to_be[i_or_a[0]].append('a')
            letters_it_has_to_be[i_or_a[1]].append('i')
            letters_it_has_to_be[i_or_a[1]].append('a')
            potential_letters = update_potential_letters(potential_letters, 'a', i_or_a)
            potential_letters = update_potential_letters(potential_letters, 'i', i_or_a)
        elif piplup == 1:
            # could be an 'i' or 'a'
            letters_it_has_to_be[i_or_a[0]].append('i')
            letters_it_has_to_be[i_or_a[0]].append('a')
        else:
            pass  # no one letter words detected

        ctext_by_word = []
        for phrase in inp_split_by_space:
            regex = re.compile('[^a-zA-Z]')
            # First parameter is the replacement, second parameter is your input string
            ctext_by_word.append(regex.sub('', phrase) + "")

        # print(ctext_by_word)

        two_letter_words = {}
        for word in ctext_by_word:
            if len(word) == 2:
                if word in two_letter_words.keys():
                    two_letter_words[word] += 1
                else:
                    two_letter_words[word] = 1
        # print(two_letter_words)
        # check_2_letter_words

        # 3 end in i
        # dui, koi, lei, psi, ski

        # 3 end in a
        # pea, ana, boa, spa, via, aha, ava, bra, sea, tea, era, yea

        opt_str = ''.join(opt_lst)
        # print(potential_letters)
        # print(letters_it_has_to_be)
        # print(opt_str)

        return []
    else:
        return []

    def encrypt(inp):
        print("Encryption for the simple substitution cipher not implemented yet.")
        exit()

    """
	for ch in characters_in_ctext:
			if ch in numericals:
				print("ERROR in substitution: Doesn't work with numericals in input.")
				return []
		
		#print(ctext)#######
		
		numtext = []
		for c in characters_in_ctext:
			numtext.append(" ")
			
		save = []
		for c in characters_in_ctext:
			save.append(c)
		counter = 0
		for ch in range(len(characters_in_ctext)):
			count = False
			if characters_in_ctext[ch] in alphabet:
				newal = alphabet.replace(characters_in_ctext[ch], "")
				alphabet = newal
				
				#print(characters_in_ctext[ch], end=' ')
				for pos in range(len(save)):
					if save[pos] == characters_in_ctext[ch]:
						numtext[pos] = counter
						count = True
						
			if count == True:
				counter += 1
		#print(numtext)
		
		frequency_in_ctext = {}
		for char in numtext:
			if str(char) != ' ':
				if str(char) in frequency_in_ctext.keys():
					frequency_in_ctext[str(char)] += 1
				else:
					frequency_in_ctext[str(char)] = 1
		#sorted frequency in ctext
		sfic = sorted(frequency_in_ctext.items(), key=operator.itemgetter(1))[::-1]
		#print(sfic)###

		for pos in range(len(english_frequency)):
			for entry in range(len(numtext)):
				try:
					if str(numtext[entry]) == sfic[pos][0]:
						numtext[entry] = english_frequency[pos]
				except IndexError:
					pass

		newtxt = "".join(numtext)		
		#print(newtxt)
		return [newtxt]
		

	#According to the unicity distance of English, 27.6 letters of ciphertext are required to crack a mixed alphabet simple substitution. 
	#In practice, typically about 50 letters are needed, although some messages can be broken with fewer if unusual patterns are found.
	elif len(ctext) > 50:
		return []	###work in progress
	else:
		print("ERROR in substitution: input is too short.")
		return []
		
		
	"""
