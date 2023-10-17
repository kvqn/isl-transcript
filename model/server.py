from io import BytesIO
from typing import Annotated
from PIL import Image
from fastapi import FastAPI, File
import tensorflow as tf
from tensorflow import keras
import base64

from model import CHARACTERS

model = keras.models.load_model("model.keras")
if model is None:
    raise Exception("Model not found.")


app = FastAPI()

@app.post("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(file: Annotated[str, File()]):
    if file.startswith('data:image/jpeg;base64,'):
        file = file[len('data:image/jpeg;base64,'):]
    base64_bytes = base64.b64decode(file)
    image = Image.open(BytesIO(base64_bytes))
    image = image.resize((256, 256))
    image = tf.keras.utils.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    prediction = CHARACTERS[model.predict(image).argmax()]
    return {"prediction": prediction}


def start_server(args):
    import uvicorn
    uvicorn.run("model.server:app", reload=args.reload)

