import pyperclip

def copier(text):
    pyperclip.copy(text)
    
if __name__ == "__main__":
    copier('test')
