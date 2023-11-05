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

    df = pd.read_csv(LANDMARKS_PATH)

    per_class = {}
    for i in CLASS_NAMES:
        per_class[i] = []

    for i in df.values:
        y = np.zeros(len(CLASS_NAMES))
        y[CLASS_NAMES.index(i[1])] = 1
        # print(y)
        x = np.asarray(i[2:]).astype("float32")
        # x = []
        # for j in range(21):
        #     x.append(_x[2 * j] ** 2 + _x[2 * j + 1] ** 2)
        # x = np.asarray(x).astype("float32")
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)
        # Y.append(y)
        # X.append(x)
        per_class[i[1]].append((x, y))

    X_train = []
    Y_train = []
    X_validation = []
    Y_validation = []

    N_TRAIN_PER_CLASS = 1
    N_VALIDATION_PER_CLASS = 1

    for i in CLASS_NAMES:
        print(f"{i}: {len(per_class[i])}")
        random.shuffle(per_class[i])
        train = pick_random_and_remove(per_class[i], N_TRAIN_PER_CLASS)
        validation = pick_random_and_remove(per_class[i], N_VALIDATION_PER_CLASS)
        x_train = [i[0] for i in train]
        y_train = [i[1] for i in train]
        x_validation = [i[0] for i in validation]
        y_validation = [i[1] for i in validation]
        X_train.extend(x_train)
        Y_train.extend(y_train)
        X_validation.extend(x_validation)
        Y_validation.extend(y_validation)

    # Z = tf.data.Dataset.from_tensor_slices((X, Y))
    # Z.shuffle(Z.cardinality())
    # Z = Z.take(2000)

    # Z_validation = Z.take(int(len(Z) * 0.8))
    # Z_train = Z.skip(int(len(Z) * 0.8))

    Z_train = tf.data.Dataset.from_tensor_slices((X_train, Y_train))
    Z_validation = tf.data.Dataset.from_tensor_slices((X_validation, Y_validation))

    model = keras.Sequential()
    model.add(layers.Input(shape=(42,)))
    # model.add(layers.Reshape((21, 2), input_shape=(42,)))
    # model.add(layers.Conv2D(21, (1, 2)))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(210))
    # model.add(layers.Dense(128), activation="relu")
    # model.add(layers.Dropout(0.3))
    model.add(layers.Activation(activation=tf.math.square))
    # model.add(layers.Dense(200, activation=tf.math.square))
    # model.add(layers.Dense(100, activation="relu"))
    model.add(layers.Dense(100, activation=tf.math.tanh))
    model.add(layers.Dense(50, activation="relu"))
    # model.add(layers.Dense(400, activation="relu"))
    # model.add(layers.Dense(800, activation="relu"))
    # model.add(layers.Dense(400, activation="relu"))
    # model.add(layers.Dense(200, activation="relu"))
    # model.add(layers.Dense(100, activation="relu"))
    # model.add(layers.Dense())
    # model.add(layers.Dense(861))
    # model.add(layers.MaxPooling1D())
    model.add(layers.Dense(len(CLASS_NAMES), activation="softmax"))

    # X = np.asarray(X)
    # Y = np.asarray(Y)

    model.compile(
        # keras.optimizers.Adam(learning_rate=0.0001),
        keras.optimizers.Adam(learning_rate=0.0001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=LOG_DIR)

    model.fit(
        Z_train,
        epochs=epochs,
        callbacks=[tensorboard_callback],
        validation_data=Z_validation,
        # batch_size=16,
    )

    model.save(model_path)

    print(f"Model saved at {model_path}")
