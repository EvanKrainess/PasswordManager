import tkinter as tk
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
window.title("Key, Value Storing System")
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

frameOptions = tk.Frame()

def handleStore():
    window.destroy()
    subprocess.Popen(['python3','store.py'])
    sys.exit()
def handleRetrieve():
    window.destroy()
    subprocess.Popen(['python3','retrieve.py'])
    sys.exit()
def handleQuit():
    window.destroy()



buttonStore = tk.Button(text = "Store Password", command = handleStore)
buttonStore.pack()
buttonRetrieve = tk.Button(text = "Retrieve Password", command = handleRetrieve)
buttonRetrieve.pack()
buttonExit = tk.Button(text = "Exit", command = handleQuit)
buttonExit.pack()
frameOptions.pack()


window.mainloop()