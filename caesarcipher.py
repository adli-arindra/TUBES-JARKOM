def cypher_enc(text):
    encrypt = ""
    for i in range (len(text)):
        lower_case = text[i].lower()
        shift = 1
        encrypt += chr(((ord(lower_case) + shift - 97) % 26) + 97)
    return encrypt

def cypher_dec(text):
    decrypt = ""
    for i in range (len(text)):
        lower_case = text[i].lower()
        shift = 25
        decrypt += chr(((ord(lower_case) + shift - 97) % 26) + 97)
    return decrypt


a = "fufUfAFa"
new = ['0' for _ in range (len(a))]
enc = cypher_enc(a)
print(enc)
dec = cypher_dec(enc)
print(dec)

