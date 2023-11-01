import os
import pandas as pd
import mediapipe as mp
from model import CLASS_NAMES, DATASET_PATH_ISL_MAIN, LANDMARKS_PATH
import cv2

hands = mp.solutions.hands.Hands(
    static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3
)

LANDMARK_NAMES = [
    "WRIST",
    "THUMB_CMC",
    "THUMB_MCP",
    "THUMB_IP",
    "THUMB_TIP",
    "INDEX_FINGER_MCP",
    "INDEX_FINGER_PIP",
    "INDEX_FINGER_DIP",
    "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP",
    "MIDDLE_FINGER_PIP",
    "MIDDLE_FINGER_DIP",
    "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP",
    "RING_FINGER_PIP",
    "RING_RINGER_DIP",
    "RING_FINGER_TIP",
    "PINKY_MCP",
    "PINKY_PIP",
    "PINKY_DIP",
    "PINKY_TIP",
]


def create_landmarks_csv(args):
    """
    Create CSV for hand landmarks from the dataset
    """

    data = []

    total = 0
    for class_name in CLASS_NAMES:
        total += len(
            os.listdir(os.path.join(DATASET_PATH_ISL_MAIN, "train", class_name))
        )

    cur = 0

    print("Processing", end="")

    for class_name in CLASS_NAMES:
        for file in os.listdir(
            os.path.join(DATASET_PATH_ISL_MAIN, "train", class_name)
        ):
            cur += 1
            print(f"\rProcessing {cur}/{total}", end="")

            img = cv2.imread(
                os.path.join(DATASET_PATH_ISL_MAIN, "train", class_name, file)
            )
            landmarks = hands.process(img).multi_hand_landmarks

            if not landmarks or len(landmarks) == 0:
                continue

            hand1 = {}
            for i, ln in enumerate(LANDMARK_NAMES):
                hand1[f"{ln}_x"] = landmarks[0].landmark[i].x
                hand1[f"{ln}_y"] = landmarks[0].landmark[i].y

            data.append({"LABEL": class_name, **hand1})

    df = pd.DataFrame(data)

    # save df
    df.to_csv(LANDMARKS_PATH)
