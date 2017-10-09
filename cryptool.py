#cryptool
import os
import argparse
import Verify

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input string or file')
parser.add_argument('-s', '--string', help='string of inp_ciphers_list', action='store_true')
parser.add_argument('-f', '--file', help='txt file with cipher', action='store_true')
parser.add_argument('-caesar', '--caesar', help='brute force caesar cipher', action='store_true')
parser.add_argument('-binary', '--binary', help='decode binary to text', action='store_true')
parser.add_argument('-b64', '--base64', help='decode base64', action='store_true')
parser.add_argument('-morse', '--morse', help='decode morse code', action='store_true')
parser.add_argument('-sbyteXOR', '--singlebyteXOR', help='decode single byte XOR', action='store_true')
parser.add_argument('-ssub', '--simplesub', help='decode substitution cipher', action='store_true')
parser.add_argument('-atb', '--atbash', help='decode atbash cipher', action='store_true')
#Potential to add: letter to number, mirror, md5, sha1...
args = parser.parse_args()

'''
When adding a new cipher:
1) add to argparse
2) add to cryptool main under arg flags
3) add values to cryptanalyzer
4) add to list under cryptanalyzer
'''




found_cryptanalyzer = True
try:
	import cryptanalyzer
except ModuleNotFoundError:
	print("Cryptanalyzer package not found.")
	found_cryptanalyzer = False


def print_plaintext(plaintext_list):
	print("-- ~ ~ ~ ~ ~ ~ ~ ~ --")
	for item in plaintext_list:
		#print(item)
		if args.file:
			print("\n"+item[2], end='')
		else:
			print("\n"+item[2])
		
		print("Cipher: "+item[0])
		for i in item[1]:
			print("Plaintext: "+i)
			
def given_cipher(cipher, ctext):
	modules = {}
	plaintext = []
	english_plaintext = []
	modules[cipher] = __import__('ciphers.' + cipher +'.' + cipher, fromlist=['*'])
	for ct in ctext:
		opt = modules[cipher].decrypt(ct, None)
		plaintext.append([cipher, opt, ct])
		if Verify.verify_english(opt) != []:
			english_plaintext.append([cipher, opt, ct])
	
	if english_plaintext != []:
		print_plaintext(english_plaintext)
	else:
		print_plaintext(plaintext)
	exit()

		
def main():
	print("--CipherTool V.0.10--")
	inp_ciphers_list = []
	decrypt = False
	encrypt = False
	lang = ["English"]
	key = None
	
	#Take input in the format of a STRING or FILE.
	#Convert input to a list.
	if args.string:
		inp_ciphers_list.append(args.input)
	elif args.file:
		with open(args.input, 'r') as file:
			inp_ciphers_list = file.readlines()###################Edit this pending input
	else:
		print("please specify -s or -f")
		exit()
	
	
	
	#If given cipher
	IMPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ciphers')
	if args.binary:
		given_cipher("binary", inp_ciphers_list)
	elif args.caesar:
		given_cipher("caesar", inp_ciphers_list)
	elif args.base64:
		given_cipher("b64", inp_ciphers_list)
	elif args.morse:
		given_cipher("morse", inp_ciphers_list)
	elif args.singlebyteXOR:
		given_cipher("singlebyteXOR", inp_ciphers_list)
	elif args.simplesub:
		given_cipher("simplesub", inp_ciphers_list)
	elif args.atbash:
		given_cipher("atbash", inp_ciphers_list)
		
		
	#Guess what cipher to use
	else:
		modules = {}
		plaintext = []
		for cipher_str in inp_ciphers_list:
			if found_cryptanalyzer == True:
				cracking_order = cryptanalyzer.cryptanalysis(cipher_str)	#orders ciphers by most likely
				#print(cracking_order)
			else:
				cracking_order = ["ceasar"] ##### Temp ##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			
			#Trys all ciphers. If decrypts, will break.
			failed_to_crack = True
			for ci in cracking_order:
				#print("Trying", ci)
				modules[ci] = __import__('ciphers.' + ci +'.' + ci, fromlist=['*'])	#get the cipher's file
				opt = modules[ci].decrypt(cipher_str, None)	#decrypt using that cipher
				
				check_decoded = Verify.verify_english(opt)	#verify that the plaintext is in english

				#verify_english returns an empty list when it does not find any english words in the opt.
				if check_decoded != []:
					plaintext.append([ci, check_decoded, cipher_str])	#print_plaintext takes a list of [the cipher, the plaintext, and the original ciphertext]
					failed_to_crack = False
					break	#exits the nested for loop. Will now try next cipher_str in inp_ciphers_list.
				else:
					pass #check the next possible cipher 
			
			
			if failed_to_crack:	############ maybe do something else here?
				plaintext.append(["FAILED", "", cipher_str])
		
		#And the final output
		print_plaintext(plaintext)
				
	exit()			
				
				
if __name__ == '__main__':
	main()	
	