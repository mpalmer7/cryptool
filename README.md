# cryptool
An identification and decryption tool for ciphers.

Run > "cryptool.py" />
For example:
> python cryptool.py -s "Khoor Zruog" <br />  for string input
> python cryptool.py -f textfile.txt <br />   for file input

The program will attempt to guess what kind of cipher you are trying to decrypt.
If you know what cipher you are decrypting, that can also be specified with one of the below flags.
> -caesar />    Caesar Cipher
> -binary />    Binary to Plaintext
> -b64 />       Base 64 to Plaintext
> -morse />     Morse Code
> -sbyteXOR />  Single Byte XOR
> -ssub />      Simple Substitution*
> -atb />       Atbash Cipher
> -rhs />       Reverse Hash, by performing a Bing search
