"""
For this wanted to check whether encrypting & decrypthing was possible without the
use of a mac_key

Issues:
If we want the mac key to be independent, 
then we would also need to require the iv and the cipherKey to be independent as well
"""

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad

def hmac_sha256(data, key):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data)
    return h.digest()


def cbc_encrypt(p, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    c = cipher.encrypt(pad(p, AES.block_size))

    return iv + c


def cbc_decrypt(c, key):
    iv = c[: AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return unpad(cipher.decrypt(c[AES.block_size :]), AES.block_size)

def encrypt_then_mac(p, iv, cipher_key, mac_key):
    cipherText=cbc_encrypt(p,iv,cipher_key)
    tag=hmac_sha256(cipherText,mac_key)
    return cipherText,tag

def verify_then_decrypt(c, t, cipher_key, mac_key):
    tag=hmac_sha256(c,mac_key)
    if(tag!=t):
    	raise ValueError("Invalid tag")
    plainText=cbc_decrypt(c,cipher_key)
    return plainText
    
def paddingIv(iv):
    print("test")
    if(len(iv)!=16 and len(iv)<16):
        print("Not 16 and smaller then 16")
        for x in range(16-len(iv)):
            iv+=' '
    if(len(iv)!=16 and len(iv)>16):
        print("Not 16 and greater then 16")
        print(iv[len(iv)-1])
        while(len(iv)!=16):
            iv=iv[:-1]
    return iv
    
def paddingCipherKey(cipher_key):
    print("test2")
    if(len(cipher_key)%16!=0):
        print("Not 16 and smaller then 16")
        while(len(cipher_key)%16!=0):
            cipher_key+=' '
    return cipher_key

if __name__=="__main__":
    """
    Test case:
    User 1:
    user_Username="1234567890123456"    (iv) (with the condition of the username being 16 chars in length) (padding is also a possibility)
    user_password="Ducks" (This acts as the Mac_key)
    
    Account 1:
        account_Username="1234567890123456"       (This acts as the cipherkey) (with the condition of the username being length%16=0 in length) (padding is also a possibility)
        account_Password="Bacon"     (this acts as the plaintext)
    """
    iv ="1234567890123456"
    iv=paddingIv(iv)
    print(len(iv))
    print(iv)
    iv=iv.encode()
    cipher_key ="1234567890123456"
    cipher_key=paddingCipherKey(cipher_key)
    print(len(cipher_key))
    print(cipher_key)
    cipher_key=cipher_key.encode()
    mac_key ="Ducks"
    mac_key=mac_key.encode()
    message ="Bacon"
    message=message.encode()
    c, t = encrypt_then_mac(message, iv, cipher_key, mac_key)
    p = verify_then_decrypt(c, t, cipher_key, mac_key)
    print(p.decode())
    