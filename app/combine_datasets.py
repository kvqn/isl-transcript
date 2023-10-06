import os
from app import (
    CHARACTERS,
    DATASET_PATH_ISL_1,
    DATASET_PATH_ISL_2,
    DATASET_PATH_ISL_3,
    DATASET_PATH_ISL_MAIN,
)
import shutil


def combine_datasets(args):
    """
    Creates the main dataset.
    Assumes that the source datasets are already downloaded and renamed as specified in the README.
    """

    dataset_path_isl_1 = DATASET_PATH_ISL_1
    dataset_path_isl_2 = DATASET_PATH_ISL_2
    dataset_path_isl_3 = DATASET_PATH_ISL_3
    dataset_path_isl_main = DATASET_PATH_ISL_MAIN

    split_ratio = args.ratio
    assert split_ratio > 0 and split_ratio < 1

    if not os.path.isdir(dataset_path_isl_main):
        os.makedirs(dataset_path_isl_main)

    for char in CHARACTERS:
        train_dir = os.path.join(dataset_path_isl_main, "train", char)
        test_dir = os.path.join(dataset_path_isl_main, "test", char)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

        train_files = []
        test_files = []

        # Dataset 1
        src_dir = os.path.join(dataset_path_isl_1, "Indian", char)
        if os.path.isdir(src_dir):
            files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]
            train_files.extend(files[: int(len(files) * split_ratio)])
            test_files.extend(files[int(len(files) * split_ratio) :])

        # Dataset 2
        src_dir = os.path.join(dataset_path_isl_2, "original_images", char)
        if os.path.isdir(src_dir):
            files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]
            train_files.extend(files[: int(len(files) * split_ratio)])
            test_files.extend(files[int(len(files) * split_ratio) :])

        # Dataset 3
        src_dir = os.path.join(dataset_path_isl_3, "Train", char)
        if os.path.isdir(src_dir):
            files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]
            train_files.extend(files[: int(len(files) * split_ratio)])
            test_files.extend(files[int(len(files) * split_ratio) :])
        src_dir = os.path.join(dataset_path_isl_3, "Test", char)
        if os.path.isdir(src_dir):
            files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]
            train_files.extend(files[: int(len(files) * split_ratio)])
            test_files.extend(files[int(len(files) * split_ratio) :])
        src_dir = os.path.join(dataset_path_isl_3, "Validation", char)
        if os.path.isdir(src_dir):
            files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]
            train_files.extend(files[: int(len(files) * split_ratio)])
            test_files.extend(files[int(len(files) * split_ratio) :])

        # Copy files
        for i, file in enumerate(train_files):
            ext = file.split(".")[-1]
            shutil.copy(file, os.path.join(train_dir, f"{i}.{ext}"))
        for i, file in enumerate(test_files):
            ext = file.split(".")[-1]
            shutil.copy(file, os.path.join(test_dir, f"{i}.{ext}"))
