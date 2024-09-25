This Python script is a basic keylogger that captures keystrokes and logs the data to Firebase Firestore in real-time. It utilizes the pynput library to monitor keyboard inputs and the firebase-admin SDK to send captured data to a Firestore database.

## Key Features:
* Keylogging: Captures both alphanumeric characters and special keys (like space, enter, etc.).
* Firebase Firestore Integration: Logs keystrokes in batches of 10 characters, including a timestamp, to Firestore for easy retrieval and analysis.
* Real-time Logging: The keylogger continuously monitors keyboard input and sends the data to Firebase as soon as the batch size is reached.
* Cross-platform: Works on Windows, macOS, and Linux systems.
  
## Requirements:
* Python 3.x
* Firebase project with Firestore database
* Firebase Admin SDK credentials (JSON file)
* pynput library for keylogging
* firebase-admin SDK for Firebase integration

## Clone the repository:

git clone https://github.com/your-repo/firebase-keylogger.git
cd firebase-keylogger

## Install the required libraries:

pip install pynput firebase-admin
Download your Firebase Admin SDK JSON key from the Firebase Console and replace the placeholder file path with the correct one in the script.

## Run the script:
python keylogger.py
## How It Works:
* Firebase Initialization: The Firebase connection is initialized using the service account key (firebase-adminsdk.json), allowing the script to interact with Firestore.
* Keystroke Capture: The script listens for key presses using pynput.keyboard. It captures all keystrokes, including special characters, and appends them to a list.
* Firebase Logging: Once the keylogger captures 10 keystrokes, it logs them to the Firestore database under a collection called keystrokes. Each entry includes:
* timestamp: When the keystrokes were logged.
* data: The captured keystrokes.
* Stopping the Keylogger: The keylogger listens continuously until the 'Esc' key is pressed, which safely terminates the script.


##Future Enhancements:
* Add encryption to the stored data for better security.
* Implement multi-threading to make the keylogging more efficient.
* Add email notifications or real-time monitoring capabilities via a dashboard.
