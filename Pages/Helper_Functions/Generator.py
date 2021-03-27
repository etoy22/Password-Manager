import random;
import numpy as np;
special = ['@','%','+','\\','/','!','#','$','^','?',':','~','-']
numbers = ['1','2','3','4','5','6','7','8','9']
upper = ['']*26
lower = ['']*26


for i in range(26):
    upper[i] = chr(65+i)
    lower[i] = chr(97+i)


def password(length,up,low,num,spec):
    output = ""
    if up + low + num + spec > 0:
        randomPasswordKeys = []
        if up == 1:
            randomPasswordKeys = np.append(randomPasswordKeys,upper)
        if low == 1:
            randomPasswordKeys = np.append(randomPasswordKeys,lower)
        if num == 1:
            randomPasswordKeys = np.append(randomPasswordKeys,numbers)
        if spec == 1:
            randomPasswordKeys = np.append(randomPasswordKeys,special)
        
        for i in range(int(length)):
            output += randomPasswordKeys[random.randint(0,len(randomPasswordKeys)-1)]
        return output
    else:
        return 'No valid password'
