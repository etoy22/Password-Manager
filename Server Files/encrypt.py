"""
For this wanted to check whether encrypting & decrypthing was possible without the
use of a mac_key

Issues:
If we want the mac key to be independent, 
then we would also need to require the iv and the cipherKey to be independent as well

Sources:Parts of the code was obtained from comp4109 challenge6
"""
import Crypto
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
    
#Checks if right cipherkey was used
def verify_then_decrypt(c, t, cipher_key, mac_key):
    tag=hmac_sha256(c,mac_key)
    if(tag!=t):
    	raise ValueError("Invalid tag")
    plainText=cbc_decrypt(c,cipher_key)
    return plainText

#Pads the iv so length=16    
def paddingIv(iv):
    if(len(iv)!=16 and len(iv)<16):
        for x in range(16-len(iv)):
            iv+=' '
    if(len(iv)!=16 and len(iv)>16):
        print(iv[len(iv)-1])
        while(len(iv)!=16):
            iv=iv[:-1]
    return iv
    
    
#Pads the CipherKey so length%16=0    
def paddingCipherKey(cipher_key):
    if(len(cipher_key)%16!=0):
        while(len(cipher_key)%16!=0):
            cipher_key+=' '
    return cipher_key

if __name__=="__main__":
    """
    Test case 1:
    User 1:
    
    user_Username="Ducks" (This acts as the Mac_key)(each username is unique so each mac_key will be unique)
    user_Password="1234567890123456"    (iv) (Needs to be 16 characters)
    
    Account 1:
        account_Username="1234567890123456"    (This acts as the cipherkey) (needs to be length%16=0)
        account_Password="Bacon"     (this acts as the plaintext)
    
    """
    
    #This is the user_Username
    mac_key ="Ducks"
    mac_key=mac_key.encode('utf=8')
    print("(user_Username)Mac_key: ",mac_key)
    #This is the user_Password and it gets padded as it needs to be "16 chars in length"
    iv ="1234567890123456"
    iv=paddingIv(iv)
    iv=iv.encode('utf-8')
    print("(user_Password)IV: ", iv)
    
    #This is the account_Username and it gets padding so its length%16=0
    cipher_key ="1234567890123456"
    cipher_key=paddingCipherKey(cipher_key)
    cipher_key=cipher_key.encode('utf-8')
    print("(account_Username)cipher_key: ", cipher_key)
    
    #This is the account_Password
    message ="Bacon"
    message=message.encode('utf-8')
    print("(account_Password)Message: ", message)
    #account_password gets encrypted 
    c, t = encrypt_then_mac(message, iv, cipher_key, mac_key)
    print("Encrypted password:", c)
    
    #account_password gets decrypted
    p = verify_then_decrypt(c, t, cipher_key, mac_key)
    print("Decrypted password:",p.decode())