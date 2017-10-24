# cryptool
An identification and decryption tool for ciphers.

Run "cryptool.py" <br />
Takes 2 inputs: <br />
    1) -s or -f (to specify string or file) <br />
    2) the string or filename. <br />
	
For example
> python cryptool.py -s "Khoor Zruog" <br />
> python cryptool.py -f textfile.txt <br />

If you know what cipher you are decrypting, that can also be specified with a flag.
Otherwise, it will try to guess what kind of cipher it is (needs a lot of work).	
