#VerifyPlaintext

#input (potential plaintext): list
#output:
#		a) list (most_likely)
#		b) empty list

def verify_english(potential_plaintext, cipher=''):
	try:
		f = open("sownew.txt", "r")
		sowpods = f.readlines()
		for d in range(len(sowpods)):
			temp = (sowpods[d].strip("\n")).lower()
			sowpods[d] = temp
		f.close
	except FileNotFoundError:
		print("ERROR in VerifyPlaintext: Could not locate dictionary file... returning empty set.")
		return []
		
	likely_plaintext = []
	for p_p in potential_plaintext:
		#split p_p into words and remove all not alphabetical characters
		working_text = p_p.split(' ')
		for n in range(len(working_text)):
			working_text[n] = ''.join([i for i in working_text[n] if i.isalpha()])
		#print(working_text)
		#if words are not seperated by spaces
		if len(working_text) == 1:
			try:
				f = open("sownew4.txt", "r")
				sowpods = f.readlines()
				for d in range(len(sowpods)):
					temp = (sowpods[d].strip("\n")).lower()
					sowpods[d] = temp
				f.close
			except FileNotFoundError:
				print("ERROR in VerifyPlaintext: Could not locate dictionary file... returning empty set.")
				return []
		
			for word in sowpods:
				if word in working_text[0]:
					likely_plaintext.append(p_p)
					
					
					
		else: #we have seperate words
			try:
				f = open("sownew.txt", "r")
				sowpods = f.readlines()
				for d in range(len(sowpods)):
					temp = (sowpods[d].strip("\n")).lower()
					sowpods[d] = temp
				f.close
			except FileNotFoundError:
				print("ERROR in VerifyPlaintext: Could not locate dictionary file... returning empty set.")
				return []
				
			for test_word in sowpods:
				for p_p_word in working_text:
					if test_word == p_p_word.lower():
						likely_plaintext.append(p_p)
						
			need_check_big = False
			for w in working_text:
				if len(w) > 6:
					need_check_big = True
			if need_check_big:
				#print("checking big words")
				try:
					f = open("7+letterwords.txt", "r")
					blw = f.readlines() #big letter words
					for d in range(len(blw)):
						temp = (blw[d].strip("\n")).lower()
						blw[d] = temp
					f.close	
					
					for test_word in blw:
						for p_p_word in working_text:
							if test_word == p_p_word.lower():
								likely_plaintext.append(p_p)
				except FileNotFoundError:
					print("ERROR in VerifyPlaintext: Could not locate big words file, ignoring it...")
					pass
						
						
						
	#decryption worked					
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
		print(potential_plaintext[0],'\t',len(potential_plaintext[0]))
		
		
		#############################
		temp = potential_plaintext[0].split(' ')
		if (max > 2) and (len(temp)>2): #accounting for mistakes...
			return most_likely
		else:
			return []
			
			
			
			
	#no english words detected
	else:
		return []
					
				
				
	return []