from io import BytesIO
from typing import Annotated
from PIL import Image
from fastapi import FastAPI, File
import tensorflow as tf
from tensorflow import keras
import base64
import numpy as np
import mediapipe as mp

from model import CHARACTERS
from model.hand_landmarks import hands

model = keras.models.load_model("model.keras")
if model is None:
    raise Exception("Model not found.")


app = FastAPI()


@app.post("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(file: Annotated[str, File()]):
    if file.startswith("data:image/jpeg;base64,"):
        file = file[len("data:image/jpeg;base64,") :]
    base64_bytes = base64.b64decode(file)
    try:
        image = Image.open(BytesIO(base64_bytes))
    except:
        return {"prediction": None}
    image = np.asarray(image)
    # image = mp.Image(format=mp.ImageFormat.SRGB, data=np.asarray(image))
    landmarks = hands.process(image).multi_hand_landmarks
    if not landmarks or len(landmarks) == 0:
        return {"prediction": None}
    landmarks = landmarks[0]
    inp = []
    for i in range(21):
        inp.append(landmarks.landmark[i].x)
        inp.append(landmarks.landmark[i].y)
    inp = np.array(inp)
    inp = inp.reshape(1, -1)
    # print(inp)
    # print(inp.shape)
    prediction = CHARACTERS[model.predict(inp).argmax()]
    return {"prediction": prediction}


def start_server(args):
    import uvicorn

    uvicorn.run("model.server:app", reload=args.reload)
