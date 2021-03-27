"""
import hashlib is a module that allows for the creation of secure hash alogorithms

This module allows to create hash objects such as SHA1,SHA2 family(SHA224,SHA256,SHA384,and SHA512)
,and SHA3 family(SHA3-224,SHA3-256,SHA3-384,SHA3-512),BLAKE2s,BLAKE2b

.encode() converts the string into bytes which is acceptable for the hash function

.update() updates the message you will be using for the hash function

.hexDigest() shows the hash value in the form of hexidecimal

Using this as password strorage:
Currently Blake2b has the strongest secuirty claim of 2^256 taking 2^256 steps to
find a collision in which its best attack is 2^224
"""
import hashlib

#Creating a sha1 object
print("SHA1")
m=hashlib.sha1()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Creating a sha224 object
print("SHA224")
m=hashlib.sha224()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Creating a sha256 object
print("SHA256")
m=hashlib.sha256()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Creating a sha384 object
print("SHA384")
m=hashlib.sha384()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Creating a sha512 object
print("SHA512")
m=hashlib.sha512()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Creating a sha3-512 object
print("SHA3-512")
m=hashlib.sha3_512()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())

#Blake2b
print("BLAKE2b")
m=hashlib.blake2b()

hashMessage=b'Hello World'
print("Hash message:",hashMessage)

m.update(hashMessage)
print("Hash value:",m.hexdigest())


