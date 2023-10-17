import os
from tensorflow import keras
from model.util import ask_bool_question
from model import DATASET_PATH_ISL_MAIN

layers = keras.layers


CLASS_NAMES = [str(i) for i in range(0, 10)] + [
    chr(i) for i in range(ord("A"), ord("Z") + 1)
]

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

    print(f"Model will be saved at {model_path}")

    data = keras.utils.image_dataset_from_directory(TRAIN_DATASET, class_names=CLASS_NAMES, label_mode="categorical")

    model = keras.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(256, 256, 3)))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(16, (3, 3), activation="relu"))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(len(CLASS_NAMES), activation="softmax"))

    model.compile("adam", loss="categorical_crossentropy", metrics=["accuracy"])

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=LOG_DIR)

    model.fit(data, epochs=4, callbacks=[tensorboard_callback])

    model.save(model_path)

    print(f"Model saved at {model_path}")
