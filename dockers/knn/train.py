from sklearn.neighbors import KNeighborsClassifier
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

host = "localhost"

id2label = {}
X_train = []
y_train = []

i = 0
for img_path in tqdm(os.listdir("images/")):
    img = cv2.imread(os.path.join("images/", img_path))

    if img is None: continue  

    img_str = encode_img(img)
    r = requests.get(f"http://{host}:7001/predict/", data=img_str, timeout=5)
    embed = r.json()["embedding"]

    id2label[i] = img_path[:-4]
    i += 1
    y_train.append(i)
    X_train.append(embed)

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

model_name = "models/knn.pkl"
pickle.dump(knn, open(model_name, 'wb'))

le_name = "models/id2label.pkl"
pickle.dump(id2label, open(le_name, 'wb'))

knn_loaded = pickle.load(open(model_name, "rb"))
le_loaded = pickle.load(open(le_name, "rb"))

print(le_loaded == id2label)

# dist, preds = knn_loaded.kneighbors(X_train, 1)

# labels = [le_loaded[pred[0]] for pred in preds]

# print(labels)
