
import cv2 as cv
import mediapipe as mp
import numpy as np
import hand as hnd
import firebase_admin
from firebase_admin import credentials, db
import os



import os
import sys

# Bungkam Qt & OpenCV warning
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

sys.stderr = open(os.devnull, "w")


# ===== FIREBASE INIT (SEKALI SAJA) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cred = credentials.Certificate(
    os.path.join(BASE_DIR, "serviceAccountKey.json")
)

firebase_admin.initialize_app(cred, {
    'databaseURL': ' ' # ISI DENGAN DATABASE URL FIREBASE
})

ref = db.reference('servo')
# =====================================

cam = cv.VideoCapture(0)
detecta = hnd.Detector()

th_id = [4,8,12,16,20]

while True:
    try:
        _, img = cam.read()
        img = detecta.findHands(img)
        lmList = detecta.findPosition_hand(img)

        if len(lmList) != 0:
            jari = []

            # Ibu jari
            jari.append(1 if lmList[th_id[0]][1] > lmList[th_id[0]-1][1] else 0)

            # Jari lain
            for i in range(1,5):
                jari.append(1 if lmList[th_id[i]][2] < lmList[th_id[i]-2][2] else 0)

            hasil = jari.count(1)
            print(hasil)

            angle_map = {
                1: 0,
                2: 45,
                3: 90,
                4: 135,
                5: 180
            }

            if hasil in angle_map:
                ref.set({'angle': angle_map[hasil]})

        cv.imshow("psychoo", img)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception as e:
        print(f"Error: {e}")

cam.release()
cv.destroyAllWindows()
