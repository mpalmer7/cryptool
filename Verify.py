#VerifyPlaintext

#input (potential plaintext): list
#output:
#		a) list (most_likely)
#		b) empty list

def verify_english(potential_plaintext, cipher=''):
	#It will often be of len(1) because most of the ciphers will just 
	#give the output.  For some ciphers, like caesar, the output is 
	#brute forced and then the results are to be narrowed down.
	
	#Import a list of scrabble words, with all words under 4 letters stripped out.
	#Also provided file with only 2/1 letter words stripped ("sownew3.txt"),
	#but I have recieved more false positives from this.
	try:
		f = open("sownew4.txt", "r")
		sowpods = f.readlines()
		for d in range(len(sowpods)):
			a = (sowpods[d].strip("\n")).lower()
			sowpods[d] = a
		f.close
	except FileNotFoundError:
		print("ERROR in VerifyPlaintext: Could not locate dictionary file... returning empty set.")
		return []
	
	#For every key combination, check every word in the english dictionary and see if it exists inside that phrase and if it does, count it by appending that key to a list
	#The plaintext that has the most "hits" of words in the dictionary list will hopefully be the plaintext.
	#actually works pretty fast
	likely_plaintext = []
	for word in sowpods:
		#print(cipher)
		for phrase in potential_plaintext: #potential_plaintext is a LIST of all of the results the decryption for the cipher returned
			if word in phrase:	############This does not account for the word appearing multiple times in the decrypted-text#########################
				likely_plaintext.append(phrase)
	#print(likely_plaintext)
	
	
	#If the decryption worked...
	if len(likely_plaintext) > 0:
		lp = {}
		#sort each phrase into the dictionary, if the phrase is already in dictionary increase count
		for word in likely_plaintext:
			if word in lp.keys():
				lp[word] += 1
			else:
				lp[word] = 1
		
		#now sort the decrypted text by count, i.e. which decrypted-text had the most words in the list of English words in it.
		max = 0
		most_likely = []
		for key in lp:
			if int(lp[key]) > max:
				most_likely = [key]
				max = lp[key]
			elif int(lp[key]) == max:	#If two words have equally the most "hits" then return them both.
				most_likely.append(key)
				
		
		return most_likely
				
				
	#If no combinations were found.  This will happen if we used the wrong cipher to decrypt, or the decryption failed.
	else:
		if cipher == "ceasar":
			return[potential_plaintext]
		else:
			return []
