import os
from app.util import ask_bool_question


def create_isl_model(args):
    """
    Creates the ISL Model and saves it in some file locally.
    Assumes that the dataset has already been combined.
    """

    model_path = args.model_path
    if os.path.exists(model_path):
        resp = ask_bool_question("Model already exists. Overwrite? [y/n]")
        if not resp:
            return

    pass


