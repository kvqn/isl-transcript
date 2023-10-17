from tensorflow import keras
from model import DATASET_PATH_ISL_MAIN, CHARACTERS
import os

TESTING_DATASET = os.path.join(DATASET_PATH_ISL_MAIN, "test")


def test_isl_model(args):
    """
    Entry point for testing the ISL Model.
    """

    model_path = args.model_path
    # Assume that the model exists

    model = keras.models.load_model(model_path)
    if not model:
        print("Model not found.")

    testing_dataset = keras.utils.image_dataset_from_directory(
        TESTING_DATASET, class_names=CHARACTERS, label_mode="categorical"
    )

    model.evaluate(testing_dataset)

