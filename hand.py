import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class Detector:
    def __init__(
        self,
        model_path="hand_landmarker.task",
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    ):
        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=maxHands,
            min_hand_detection_confidence=detectionCon,
            min_hand_presence_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def findHands(self, img, draw=True):
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        self.result = self.detector.detect(mp_image)

        if draw and self.result.hand_landmarks:
            for hand_landmarks in self.result.hand_landmarks:
                for lm in hand_landmarks:
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv.circle(img, (cx, cy), 8, (255, 0, 0), cv.FILLED)

        return img

    def findPosition_hand(self, img, handNo=0):
        lmList = []

        if self.result.hand_landmarks and handNo < len(self.result.hand_landmarks):
            hand = self.result.hand_landmarks[handNo]
            h, w, _ = img.shape

            for idx, lm in enumerate(hand):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([idx, cx, cy])

        return lmList
