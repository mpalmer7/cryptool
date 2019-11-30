def decrypt(inp_obj):
    yield inp_obj.string[::-1]


def encrypt(inp_obj):
    return inp_obj.string[::-1]
