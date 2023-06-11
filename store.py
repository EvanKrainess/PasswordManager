import tkinter as tk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import sqlite3
import sys
import subprocess
import random

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    website TEXT UNIQUE,
    username BLOB,
    password BLOB,
    iv BLOB
)
""")
conn.commit()

window = tk.Tk()
window_width = 600
window_height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.title("Create a master password")
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

frameStore = tk.Frame(window)

websiteLabel = tk.Label(frameStore, text="Website")
websiteLabel.pack()
websiteEntry = tk.Entry(frameStore)
websiteEntry.pack()

usernameLabel = tk.Label(frameStore, text="Username")
usernameLabel.pack()
usernameEntry = tk.Entry(frameStore)
usernameEntry.pack()

passwordLabel = tk.Label(frameStore, text="Password")
passwordLabel.pack()
passwordEntry = tk.Entry(frameStore)
passwordEntry.pack()

def handleStore():
    website = str(websiteEntry.get())
    username = str(usernameEntry.get())
    password = str(passwordEntry.get())

    # Load the encryption key
    with open("key.bin", "rb") as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC)

    # Pad the username and password
    padded_username = pad(username.encode('utf-8'), AES.block_size)
    padded_password = pad(password.encode('utf-8'), AES.block_size)

    # Encrypt the padded data
    encrypted_username = cipher.encrypt(padded_username)
    encrypted_password = cipher.encrypt(padded_password)

    iv = cipher.iv
    try:
        # Store the encrypted data as binary in the database
        cursor.execute("""
        INSERT INTO passwords (website, username, password, iv)
        VALUES (?, ?, ?, ?)
        """, (website, encrypted_username, encrypted_password, iv))
        conn.commit()

        storeLabel.configure(text = "Stored!")
    except:
        storeLabel.configure(text = "Updated Information")
        cursor.execute("""
        UPDATE passwords
        SET username = (?), password = (?), iv = (?)
        WHERE website = (?)
        """,(encrypted_username,encrypted_password,iv,website))
        conn.commit()


storeButton = tk.Button(frameStore, text="Store", command=handleStore)
storeButton.pack()

storeLabel=tk.Label(master = frameStore)
storeLabel.pack()

def handleBack():
    window.destroy()
    cursor.close()
    conn.close()
    subprocess.Popen(['python3','home.py'])
    sys.exit()

backButton = tk.Button(master = frameStore,text = "Back", command = handleBack)
backButton.pack()

def handleGenerate():
    str = ""
    for i in range(14):
        r = random.randint(33,126)
        str+=chr(r)
    print(str)
    passwordEntry.delete(0,tk.END)
    passwordEntry.insert(0,str)


generateButton = tk.Button(master = frameStore, text = "Generate a password", command = handleGenerate )
generateButton.pack()


frameStore.pack()

window.mainloop()
