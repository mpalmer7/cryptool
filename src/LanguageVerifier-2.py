# from nltk.corpus import words
import enchant

d = enchant.Dict('en_US')

string = 'thispodcastisawonderfulwaytopasstimeduringroadtrips'
string = input()


def recursion(i, string):
    branches = {}
    found_words = []
    for j in range(i + 1, len(string) + 1):  # checks from current index in string to end of string
        # For some reason, every 1-letter word is a "real" word; hardcoded fix
        if string[i:j] == "a" or string[i:j] == "i":
            found_words.append(string[i:j])
        elif len(string[i:j]) > 1:

            # find every word
            if d.check(string[i:j]):
                found_words.append(string[i:j])
    for word in found_words:
        branches[word] = recursion(i + len(word), string)
    return branches


def fix_branches(d, curstr=""):
    ls = []
    for word in d:
        newstr = curstr + " " + word
        if d[word]:
            ls.extend(fix_branches(d[word], newstr))
        else:
            ls.append(newstr)
    return ls


branches = recursion(0, string)

max_len = 0
plaintext = ''
pt_word_count = 99999999
for branch in fix_branches(branches):
    b_len = len("".join(branch.split(" ")))
    if b_len > max_len:
        max_len = b_len
        plaintext = branch
        pt_word_count = len(branch.split(" "))
    elif b_len == max_len:
        if len(branch.split(" ")) < pt_word_count:
            pt_word_count = len(branch.split(" "))
            plaintext = branch
print(plaintext)

# if max_len != len_of_inp
#   for string in fix_branches
#       index = len(string) + 1
#       input[index] = red (ignored)
#
#       new_inp = input[index:]
#       recursion(new_input)