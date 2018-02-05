# cryptool
An identification and decryption tool for ciphers.

Run `cryptool.py` <br />
For example: <br />
`>> python cryptool.py -s "Khoor Zruog"`  for string input <br />
`>> python cryptool.py -f textfile.txt`   for file input <br />

The program will attempt to guess what kind of cipher you are trying to decrypt. <br />
If you know what cipher you are decrypting, that can also be specified with one of the below flags: <br />
`caesar`     Caesar Cipher <br />
`-binary`    Binary to Plaintext <br />
`-b64`       Base 64 to Plaintext <br />
`-morse`     Morse Code <br />
`-sbyteXOR`  Single Byte XOR <br />
`-ssub`      Simple Substitution* <br />
`-atb`       Atbash Cipher <br />
`-rhs`       Reverse Hash, by performing a Bing search*
`-revtext`	 Reverse (or flip) the string <br />

*Work in Progress
