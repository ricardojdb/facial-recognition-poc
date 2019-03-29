from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

import numpy as np 
import requests
import base64
import pickle 
import cv2
import os

def encode_img(img):
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)
    return img_str

dataset = {}

host = "192.168.1.129"

for img_path in tqdm(os.listdir("images/")):
    img = cv2.imread(os.path.join("images/", img_path))

    if img is None: continue  

    img_str = encode_img(img)
    r = requests.get(f"http://{host}:7000/predict/", data=img_str, timeout=5)
    embed = r.json()["embedding"]

    dataset[img_path[:-4]] = embed

le = LabelEncoder()
X_train = list(dataset.values())
y_train = list(dataset.keys())

y_train = le.fit_transform(y_train)

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

model_name = "models/knn.pkl"
pickle.dump(knn, open(model_name, 'wb'))

le_name = "models/label_encoder.pkl"
pickle.dump(le, open(le_name, 'wb'))

# dist, preds = knn.kneighbors(X_train, 1)

# knn_loaded = pickle.load(open(model_name, "rb"))
# le_loaded = pickle.load(open(le_name, "rb"))

# dist, preds = knn_loaded.kneighbors(X_train, 1)

# labels = le_loaded.inverse_transform(np.reshape(preds, (-1,)))

# print(labels)
