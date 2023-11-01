import os
from tensorflow import keras
from model.util import ask_bool_question
from model import DATASET_PATH_ISL_MAIN, CLASS_NAMES, LANDMARKS_PATH
import pandas as pd
import numpy as np
import tensorflow as tf

layers = keras.layers


TRAIN_DATASET = os.path.join(DATASET_PATH_ISL_MAIN, "train")

LOG_DIR = "logs"


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
        resp = ask_bool_question("Model already exists. Overwrite? [y/n]")
        if not resp:
            return

    epochs = args.epochs

    print(f"Model will be saved at {model_path}")

    df = pd.read_csv(LANDMARKS_PATH)

    Y = []
    X = []

    for i in df.values:
        y = np.zeros(len(CLASS_NAMES))
        y[CLASS_NAMES.index(i[1])] = 1
        # print(y)
        x = np.asarray(i[2:]).astype("float32")
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)
        Y.append(y)
        X.append(x)

    Z = tf.data.Dataset.from_tensor_slices((X, Y))
    Z.shuffle(Z.cardinality())

    model = keras.Sequential()
    model.add(layers.Dense(256, input_shape=(X[0].shape[1],)))
    model.add(layers.Dense(256))
    model.add(layers.Dense(256))
    model.add(layers.Dense(256))
    model.add(layers.Dense(256))
    model.add(layers.Dense(256))
    model.add(layers.Dense(len(CLASS_NAMES), activation="softmax"))

    # X = np.asarray(X)
    # Y = np.asarray(Y)

    model.compile("adam", loss="categorical_crossentropy", metrics=["accuracy"])

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=LOG_DIR)

    model.fit(Z, epochs=epochs, callbacks=[tensorboard_callback])

    model.save(model_path)

    print(f"Model saved at {model_path}")
