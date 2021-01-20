import re
import enchant


class Language:
    def __init__(self, lang_name):
        self.name = lang_name
        if lang_name == "english":
            self.lang = enchant.Dict('en_US')
        else:  # todo implement support for other languages
            print("Only english is implemented so far, sorry.  Using english.")
            self.lang = enchant.Dict('en_US')

    # ToDo - get a better dictionary or fix that every two character is legit
    # ToDo - allow the recursion to skip letters and check further
    #           - i.e. If you hit a non-english word like "YMCA" it'll end the branching there...
    # ToDo - allow a wordlist as an input; eg ctf{ or flag{ as valid words
    def verify_string(self, inp_s):
        # 1. REMOVE NON-ALPHABETICAL CHARACTERS -----------------------------------------------------------------------#
        s = re.sub(r'\W+', '', inp_s)  # todo how does this work in other character sets?
        # print(s)

        # 2. CREATE ALL WORD POSSIBILITIES ----------------------------------------------------------------------------#
        nested_branches = self._recursively_find_words(0, s)
        branches = self._fix_branches(nested_branches)
        # print(branches)

        # 3. IDENTIFY THE BEST BRANCH ---------------------------------------------------------------------------------#
        plaintext = self._find_best_branch(branches)
        # print(plaintext)

        # 4. CHECK IF INPUT WAS LEGIT ---------------------------------------------------------------------------------#
        avg_word_len = 5  # ToDo arbitrary
        expected_num_words = len(s) / avg_word_len
        words_found = len(plaintext.split(" ")) - 1  # counts spaces not words; which is + 1
        # print(f"Expected number of words: {expected_num_words}")
        # print(f"Words found: {words_found}")

        if words_found > expected_num_words:
            return True
        else:
            return False

    def _recursively_find_words(self, i, string):
        branches = {}
        found_words = []
        for j in range(i + 1, len(string) + 1):  # checks from current index in string to end of string
            # For some reason, every 1-letter word is a "real" word; hardcoded fix
            if string[i:j] == "a" or string[i:j] == "i":
                found_words.append(string[i:j])
            elif len(string[i:j]) > 1:

                # find every word
                if self.lang.check(string[i:j]):
                    found_words.append(string[i:j])
        for word in found_words:
            branches[word] = self._recursively_find_words(i + len(word), string)
        return branches

    # Converts nested dictionary to strings
    def _fix_branches(self, nested_branches, curstr=''):
        ls = []
        for word in nested_branches:
            newstr = curstr + " " + word
            if nested_branches[word]:
                ls.extend(self._fix_branches(nested_branches[word], newstr))
            else:
                ls.append(newstr)
        return ls

    def _find_best_branch(self, branches):
        max_len = 0
        plaintext = ''
        pt_word_count = 99999999
        for branch in branches:
            b_len = len("".join(branch.split(" ")))
            if b_len > max_len:  # ID the branch with the most characters used
                max_len = b_len
                plaintext = branch
                pt_word_count = len(branch.split(" "))
            elif b_len == max_len:  # If two branches have most characters, use one with the least amount of words
                if len(branch.split(" ")) < pt_word_count:
                    pt_word_count = len(branch.split(" "))
                    plaintext = branch
        # print(plaintext)
        return plaintext
