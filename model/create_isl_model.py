import os
from tensorflow import keras
from model.util import ask_bool_question
from model import DATASET_PATH_ISL_MAIN, CLASS_NAMES, LANDMARKS_PATH
import pandas as pd
import numpy as np
import tensorflow as tf
import random

layers = keras.layers


TRAIN_DATASET = os.path.join(DATASET_PATH_ISL_MAIN, "train")

LOG_DIR = "logs"


def pick_random_and_remove(arr, n):
    if n > len(arr):
        raise ValueError("n cannot be greater than the number of elements in the array")

    picked_elements = []
    for _ in range(n):
        index = random.randrange(len(arr))
        picked_elements.append(arr.pop(index))

    return picked_elements


def create_isl_model(args):
    """
    Creates the ISL Model and saves it in some file locally.
    Assumes that the dataset has already been combined.
    """

    model_path = os.path.abspath(args.model_path)
    if not model_path.endswith(".keras"):
        print("Model path must end with .keras")
        return
    if not os.path.isdir(os.path.dirname(model_path)):
        print("Enter a valid path for the model.")
        return
    if os.path.exists(model_path):
        resp = ask_bool_question("Model already exists. Overwrite? [y/n] ")
        if not resp:
            return

    epochs = args.epochs

    print(f"Model will be saved at {model_path}")

    data = keras.utils.image_dataset_from_directory(
        TRAIN_DATASET, class_names=CLASS_NAMES, label_mode="categorical"
    )

    data.shuffle(data.cardinality())

    data_train = data.take(100)
    data_validation = data.skip(100).take(10)

    model = keras.Sequential()
    model.add(layers.Conv2D(4, (4, 4), activation="relu", input_shape=(256, 256, 3)))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(2, (4, 4), activation="relu"))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(len(CLASS_NAMES), activation="softmax"))

    model.compile("adam", loss="categorical_crossentropy", metrics=["accuracy"])

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=LOG_DIR)

    model.fit(
        data_train,
        epochs=epochs,
        callbacks=[tensorboard_callback],
        validation_data=data_validation,
    )

    model.save(model_path)

    print(f"Model saved at {model_path}")
