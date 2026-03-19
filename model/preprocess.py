# model/preprocess.py

import pickle

def load_model():
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)