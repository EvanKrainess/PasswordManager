import subprocess
import sys

keyExists = False

try:
    with open("key.bin", 'rb'):
        keyExists = True

except:
    pass

if(keyExists):
    subprocess.Popen(['python3','login.py'])
    sys.exit()
else:
    subprocess.Popen(['python3','newUser.py'])
    sys.exit()
