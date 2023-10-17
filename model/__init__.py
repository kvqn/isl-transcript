import os

CHARACTERS = [str(i) for i in range(0, 10)] + [
    chr(i) for i in range(ord("A"), ord("Z") + 1)
]

DATASET_PATH_ISL_1 = os.path.join("dataset", "1")
DATASET_PATH_ISL_2 = os.path.join("dataset", "2")
DATASET_PATH_ISL_3 = os.path.join("dataset", "3")
DATASET_PATH_ISL_MAIN = os.path.join("dataset", "main", "isl")
