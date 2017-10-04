#substitution (maybe call frequencyanalysis?)

'''
Substitution cipher
Like caesar except no rotation
Pick randomly which letters to substitute
    a->z    b->c

Breaking substitution
can’t brute force
frequency analysis
quipqiup
'''
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

sys.path.append(dir_path)
import caesar 

def decrypt(ctext, nullthing=None):
	both_alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	characters_in_ctext = list(ctext)
	
	print(characters_in_ctext)
	
	n = 0
	
	
	for ch in range(len(characters_in_ctext)):
		if str(characters_in_ctext[ch]) in both_alphabets:
			
			newtext = ctext.replace(characters_in_ctext[ch], str(n))
			ctext = newtext
			
		n+=1

	#print(newtext)
	
	pt = ''
	mydict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z'}
	for letter in list(newtext):
		if str(letter) in mydict.keys():
			pt += str(mydict.get(str(letter)))
		else:
			pt += str(letter)
			
	#print(pt)
	return caesar.decrypt(pt, None)
