import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
min_percent = 0
max_percent = 100

cap = cv2.VideoCapture(0)

def generate_frames():

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    min_percent = 0
    max_percent = 100

    try:
        with open("calibration.txt","r") as f:
            data = f.read().split(",")
            min_percent = int(data[0])
            max_percent = int(data[1])
    except:
        pass

    vol_percent = 0   # <-- ADD THIS

    while True:
        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                lmList = []

                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append((cx,cy))

                if len(lmList) != 0:

                    x1,y1 = lmList[4]
                    x2,y2 = lmList[8]

                    cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
                    cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
                    cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

                    length = np.hypot(x2-x1,y2-y1)

                    system_vol = np.interp(vol_percent,[0,100],[minVol,maxVol])
                    vol_percent = np.interp(length,[30,200],[min_percent,max_percent])

                    volume.SetMasterVolumeLevel(system_vol,None)
                    cv2.putText(img, f'Volume: {int(vol_percent)} %', (40,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')