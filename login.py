import tkinter as tk

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

import subprocess
import sys
#Window settings

window = tk.Tk()
window_width = 300
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.title("Login")
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

loginFrame = tk.Frame()

def handleLogin():
    password = str(passwordEntry.get())
    with open("key.bin", "rb") as f:
        realKey = f.read()
    with open("salt.bin", "rb") as f:
        salt = f.read()
    attemptKey = PBKDF2(password,salt,dkLen =32)
    if(attemptKey == realKey):
        window.destroy()
        subprocess.Popen(['python3','home.py'])
        sys.exit()
    else:
        errorLabel.pack_forget()
        errorLabel.pack()
    
    

loginLabel = tk.Label(master = loginFrame,text = "Enter your password")
loginLabel.pack()

passwordEntry = tk.Entry(master = loginFrame, show="*")
passwordEntry.pack()

loginButton = tk.Button(master = loginFrame, text = "Login", command = handleLogin)
loginButton.pack()

errorLabel = tk.Label(master = loginFrame, text = "Wrong Password")

loginFrame.pack()




window.mainloop()