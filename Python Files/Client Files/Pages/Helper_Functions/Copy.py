import pyperclip

def copier(text):
    '''
    Send text in and it will be copied to the users clipboard
    '''
    pyperclip.copy(text)
    
if __name__ == "__main__":
    copier('test')
