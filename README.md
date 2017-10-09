# cryptool
An identification and decryption tool for ciphers.

Run "cryptool.py"
Takes 2 inputs:
	1) -s or -f (to specify string or file)
	2) the string or filename.
	
For example
> python cryptool.py -s "Khoor Zruog"
> python cryptool.py -f textfile.txt

If you know what cipher you are decrypting, that can also be specified with a flag.
Otherwise, it will try to guess what kind of cipher it is (needs a lot of work).	

## ToDo
-clean up code
-implement an option to encrypt plaintext
-fix false positives verifying that caesar cipher decrypted correctly
-update cryptanalyzer
-add in more ciphers
-get simple substitution cipher working

