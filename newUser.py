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
window.title("Create a master password")
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')



framePassword = tk.Frame()

def handleCreate():
    pass1 = str(entryPassword.get())
    pass2 = str(confirmPassword.get())
    if(pass1 != pass2):
        errorLabel.pack_forget()
        errorLabel.pack()
        
    else:
        errorLabel.pack_forget()
        print("good")
        salt = get_random_bytes(32)
        with open("salt.bin", "wb") as f:
            f.write(salt)
        password = str(entryPassword.get())
        key = PBKDF2(password,salt,dkLen =32)
        with open("key.bin", "wb") as f:
            f.write(key)
        window.destroy()
        subprocess.Popen(['python3','login.py'])
        sys.exit()



labelPassword = tk.Label(text = "Enter a master password",master = framePassword)
labelPassword.pack()

entryPassword = tk.Entry(master = framePassword, show ="*")
entryPassword.pack()

labelPasswordConf = tk.Label(master = framePassword,text = "Re-enter master password")
labelPasswordConf.pack()

confirmPassword = tk.Entry(master = framePassword, show ="*")
confirmPassword.pack()

createButton = tk.Button(master = framePassword, text = "Create password!", command = handleCreate)
createButton.pack()

errorLabel = tk.Label(text = "Passwords are not the same",master = framePassword)

framePassword.pack()

window.mainloop()

