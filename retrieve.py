import tkinter as tk
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sqlite3
import subprocess
import sys

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

window = tk.Tk()
window_width = 300
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.title("Create a master password")
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

frameRetrieve = tk.Frame(window)

websiteLabel = tk.Label(frameRetrieve, text="Enter a website you would like the info of")
websiteLabel.pack()

entryWebsite = tk.Entry(frameRetrieve)
entryWebsite.pack()

usernameLabel = tk.Label(frameRetrieve, text="")
usernameLabel.pack()

passwordLabel = tk.Label(frameRetrieve, text="")
passwordLabel.pack()

def handleRetrieve():
    website = entryWebsite.get()

    cursor.execute("""
    SELECT * FROM passwords WHERE website = (?)
    """, [website])
    results = cursor.fetchone()

    if results is None:
        usernameLabel.configure(text="Sorry, you do not have a password for that website")
    else:
        with open("key.bin", 'rb') as f:
            key = f.read()

        encrypted_username = results[1]
        encrypted_password = results[2]
        iv = results[3]

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)

        # Decrypt the data and unpad it
        decrypted_username = unpad(cipher.decrypt(encrypted_username), AES.block_size).decode('utf-8')
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')

        usernameLabel.configure(text=f"Username: {decrypted_username}")
        passwordLabel.configure(text=f"Password: {decrypted_password}")



retrieveButton = tk.Button(frameRetrieve, text="Retrieve", command=handleRetrieve)
retrieveButton.pack()

def handleBack():
    window.destroy()
    cursor.close()
    conn.close()
    subprocess.Popen(['python3','home.py'])
    sys.exit()

backButton = tk.Button(master = frameRetrieve,text = "Back", command = handleBack)
backButton.pack()


frameRetrieve.pack()

window.mainloop()
