# cryptool
An identification and decryption tool for ciphers.

Run `cryptool.py` <br />
For example: <br />
`>> python cryptool.py -s "Khoor Zruog"`  for string input <br />
`>> python cryptool.py -f textfile.txt`   for file input <br />
-f will interpret the file line by line. <br />

Optional Flags:
`-key` add to specify a key to encrypt/decrypt with. <br />
`-cic` add to check if the cipher-text was encrypted with multiple different ciphers. <br />

The program will attempt to guess what kind of cipher you are trying to decrypt. <br />
If you know what cipher you are decrypting, that can also be specified with one of the below flags. <br />

__Substitution Ciphers__ <br />
`-caesar`           Caesar Cipher <br />
`-atb`              Atbash Cipher <br />
`-vigenere`    Vigenère Cipher <br />
(WIP)`-mono`        Monoalphabetic (Simple) Substitution <br />
(TODO) `-playfair`  Playfair Cipher <br />
(TODO) `-hill`      Hill Cipher <br />
(TODO) `-vernam`    Vernam Cipher <br />

__Other__ <br />
`-binary`    Binary to Plaintext <br />
`-b64`       Base 64 to Plaintext <br />
`-morse`     Morse Code <br />
`-sbyteXOR`  Single Byte XOR <br />
`-revtext`	 Reverse (or flip) the string <br />
(WIP)`-rhs`       Reverse Hash, by performing a DuckDuckGo search <br />
