def encrypt(text):
    ret = ""
    for i in range (len(text)):
        shift = 23
        ret += chr(ord(text[i]) + shift)
    return ret

def decrypt(text):
    ret = ""
    for i in range (len(text)):
        shift = 23
        ret += chr(ord(text[i]) - shift)
    return ret
