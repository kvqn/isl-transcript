# ISL Transcript

Tested on Python 3.11.5

## Setup and Installation

### Downloading the appropriate packages

The project requires the use of python and nodejs. The preferred versions are
Python 3.11.5 and NodeJS 18.18.0 because that is what the software was tested
on, although any stable version of the packages should work.

### Install the requirements

Install the python and nodejs requirements.

```
pip install -r requirements.txt
cd app
npm i
```

## Dataset

The dataset is created by combining 3 datasets from Kaggle.

```
dataset/
    1/
        Indian/
    2/
        original_images/
    3/
        Test/
        Train/
        Validation/
    main/ (created by the CLI by combining the 3 datasets)
        test/
        train/
```

Download the following datasets and then rename their extracted folders 1, 2,
3, respectively.

1. https://www.kaggle.com/datasets/prathumarikeri/indian-sign-language-isl

1. https://www.kaggle.com/datasets/atharvadumbre/indian-sign-language-islrtc-referred

1. https://www.kaggle.com/datasets/saurabh24999/indian-sign-language

https://drive.google.com/file/d/1-zWChpYrN-n3ULJNtPWQaot2uvCcFNAn/view?usp=drive_link

### Combining the dataset

```
python -m model combine-datasets [--ratio] [--images-per-class]
```

### Create the model

```
python -m model create-isl-model
```

### Test the model

```
python -m model test-isl-model
```

### Run the python server

```
python -m model start-server
```

The python server will serve as the backend, providing the prediction
functionality to the NextJS Server

### Build and Start the NextJS Server

```
cd app
npm run build
npm run start
```
