import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

recognizer = sr.Recognizer()
mic = sr.Microphone()


def listen_command():
    try:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

        command = recognizer.recognize_google(audio,language='en-IN').lower()
        print("You said:", command)

        return command

    except Exception as e:
        print("Error:", e)
        return None


def process_command(command):

    if command is None:
        return "No command detected"

    command = command.lower().strip()

    print("Processed:", command)

    # ✅ STRICT matching
    if command == "mute":
        volume.SetMute(1, None)
        return "Muted 🔇"

    elif command == "unmute":
        volume.SetMute(0, None)
        return "Unmuted 🔊"

    elif command == "volume up":
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        return "Volume Increased 🔊"

    elif command == "volume down":
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        return "Volume Decreased 🔉"

    else:
        return "Command not recognized ❌"