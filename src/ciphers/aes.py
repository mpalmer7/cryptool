# ToDo cant find library. Tried crypto, pycryptodome, pycrypto
# from Crypto import Random
# from Crypto.Cipher import AES

"""
class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
"""

def decrypt(inp_obj):
    print("AES decryption not implemented yet.")
    yield None

    # aes_obj = AESCipher(inp_obj.key)
    # yield aes_obj.decrypt(inp_obj.bytes)


def encrypt(inp_obj):
    print("AES encryption not implemented yet.")
    yield None

    # aes_obj = AESCipher(inp_obj.key)
    # return aes_obj.encrypt(inp_obj.string)
