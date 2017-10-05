#substitution
import operator
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

#Test Case: giuifg cei iprc tpnn du cei qprcni

def decrypt(ctext, nullthing=None): 
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	numericals = "0123456789"
	symbols = " !@#$%^&*()-_+=\\|\"':;<>,.?/[]{}"
	characters_in_ctext = list(ctext.lower())
	
	#print(ctext)
	#print(characters_in_ctext)
	
	
	if len(ctext) > 2000:	#2000 arbitrary... to fix###########################
		english_frequency = ['e','t','a','o','i','n','s','h','r','d','l','u','c','m','w','f','g','y','p','b','v','k','j','x','q','z']
		
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
	elif len(ctext > 50):
		return []	###work in progress
	else:
		print("ERROR in substitution: input is too short.")
		return []
		
		
		
		
		
		
		
		
		
		
		