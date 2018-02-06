'''
When adding a new cipher:
1) add to argparse
2) add to cryptool main under arg flags
3) add values to cryptanalyzer
4) add to list under cryptanalyzer
5) update readme
'''

import os
import argparse
import Verify
import shutil #used in print_plaintext

try:
	import cryptanalyzer
	found_cryptanalyzer = True
except ModuleNotFoundError:
	print("Cryptanalyzer package not found.")
	found_cryptanalyzer = False

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file or string')
parser.add_argument('-s', '--string', help='string of ciphertext', action='store_true')
parser.add_argument('-f', '--file', help='text file of ciphertext', action='store_true')

parser.add_argument('-caesar', '--caesar', help='decode using caesar cipher', action='store_true')
parser.add_argument('-binary', '--binary', help='convert binary to plaintext', action='store_true')
parser.add_argument('-b64', '--base64', help='decode base64', action='store_true')
parser.add_argument('-morse', '--morse', help='decode morse code', action='store_true')
parser.add_argument('-sbyteXOR', '--singlebyteXOR', help='decode single byte XOR', action='store_true')
parser.add_argument('-ssub', '--simplesub', help='decode substitution cipher', action='store_true')
parser.add_argument('-atb', '--atbash', help='decode atbash cipher', action='store_true')
parser.add_argument('-rhs', '--hashsearch', help='search Bing for a hash', action='store_true')
parser.add_argument('-revtext', '--reversetext', help='Reverse a string', action='store_true')
args = parser.parse_args()


def print_plaintext(plaintext_list):
	columns, lines = shutil.get_terminal_size((80, 20))
	for item in plaintext_list:
		print("#"*columns+"Cipher Text:\n\t"+item[2]+"\nCipher:\n\t"+item[0]+"\nPlaintext:")
		if len(item[1])==0:
			print("\tDECRYPTION FAILED")
		else:
			for i in item[1]:
				print("\t"+i)
	print("#"*columns)
	return None
			
def given_cipher(cipher, ctext_list):
	p_p, e_p = [], [] #potential_plaintext, english_plaintext
	module = __import__('ciphers.' + cipher +'.' + cipher, fromlist=['*'])
	for ct in ctext_list:
		opt = module.decrypt(ct, None)
		p_p.append([cipher, opt, ct])
		if Verify.verify_english(opt, cipher) != []:
			e_p.append([cipher, opt, ct])
	if e_p != []:
		print_plaintext(e_p)
	else:
		print_plaintext(p_p)
	exit()
	
def check_ciphers(cipher, cipher_str):
	opt = __import__('ciphers.' + cipher +'.' + cipher, fromlist=['*']).decrypt(cipher_str, None)	#get the cipher's file and decrypt using that cipher
	check_decoded = Verify.verify_english(opt, cipher)	#verify that the plaintext is in english
	if check_decoded != []: #returns empty list if it could not verify
		
		print("Did the %s decryption work? Output:" % cipher)
		for str in check_decoded:
			print(str)
		while 1 == 1: #I realize this is ugly
			temp = input("(Y/N): ")
			if temp.lower() == "n":
				return None
			elif temp.lower() == "y": #decryption sucessful
				failed_to_crack = False
				return [cipher, check_decoded, cipher_str] #[the cipher, the plaintext, and the original ciphertext]
			else:
				print("Input not reconized, please try again.")

		
def main():
	inp_ciphers_list = []
	decrypt, encrypt = False, False
	key = None

	#Take user input (file or string)
	if args.string:
		if args.file:
			print("please specify -s or -f")
			exit()
		inp_ciphers_list.append(args.input)
	elif args.file: ###################Edit this pending input... currently reads by lines
		with open(args.input, 'r') as file:
			icl = file.readlines()
			for c in icl:
				inp_ciphers_list.append(c[:-1]) #removes '\n'
	else:
		print("please specify -s or -f")
		exit()
	
	#If given cipher
	IMPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ciphers')
	if args.binary:
		given_cipher("binary", inp_ciphers_list)
	if args.caesar:
		given_cipher("caesar", inp_ciphers_list)
	if args.base64:
		given_cipher("b64", inp_ciphers_list)
	if args.morse:
		given_cipher("morse", inp_ciphers_list)
	if args.singlebyteXOR:
		given_cipher("singlebyteXOR", inp_ciphers_list)
	if args.simplesub:
		given_cipher("simplesub", inp_ciphers_list)
	if args.atbash:
		given_cipher("atbash", inp_ciphers_list)
	if args.hashsearch:
		given_cipher("hashsearch", inp_ciphers_list)
	if args.reversetext:
		given_cipher("reversetext", inp_ciphers_list)
	#guess what cipher to use
	else:
		plaintext = []
		for cipher_str in inp_ciphers_list:
			if found_cryptanalyzer == True:
				cracking_order = cryptanalyzer.cryptanalysis(cipher_str)
			else:
				cracking_order = ["binary", "b64", "morse", "singlebyteXOR", "subtypeciphers", "hashsearch"] ##### Temp #####
			#Trys to decrypt using every cipher; stops when successful
			failed_to_crack = True
			
			for cipher in cracking_order:
				checker = check_ciphers(cipher, cipher_str)
				if checker != None:
					plaintext.append(checker)
					failed_to_crack = False
					break
				#else, decryption failed, try next cipher
			if failed_to_crack:
				plaintext.append(["FAILED", "", cipher_str])
		print_plaintext(plaintext)	
	exit()			
				
if __name__ == '__main__':
	print("--CipherTool V.0.30--")
	main()	
	