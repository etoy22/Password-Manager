import random;
import numpy as np;

# All characters that will be randomized
special = ['@','%','+','\\','/','!','#','$','^','?',':','~','-']
numbers = ['1','2','3','4','5','6','7','8','9']
upper = ['']*26
lower = ['']*26

#set up for uppercase and lowercase letters
for i in range(26):
    upper[i] = chr(65+i)
    lower[i] = chr(97+i)


def password(length,up=1,low=1,num=1,spec=1):
    '''
    This takes the the desires of the user interms of length, uppercase, lowercase and special numbers
    and gives them a random password wit those specifications
    '''
    output = ""
    #Checking if there is a valid random password
    if up + low + num + spec > 0:
        randomPasswordKeys = []
        #Adding to the pool of random possiblities
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
