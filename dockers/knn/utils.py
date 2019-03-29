from io import BytesIO
import numpy as np
import requests
import pickle
import base64
import json
import os 

global device

class KnnModel(object):
    def __init__(self, models_path, vgg_host):
        self.vgg_host = vgg_host
        self.models_path = models_path
        self.model = self.init_model("knn.pkl")
        self.label_encoder = self.init_model("label_encoder.pkl")
    
    def init_model(self, model_name):
        path = os.path.join(self.models_path, model_name)
        return pickle.load(open(path, 'rb'))

    def who_is_it(self, embed):   
        dist, label = self.model.kneighbors([embed])
        dist, label = dist[0,0], label[0,0]
        if dist > 1.05:
            label = "Unknown"
        else:
            label = self.label_encoder.inverse_transform([label])[0]
        return dist, label 

    def model_predict(self, data):
        preds = requests.get(f'http://{self.vgg_host}/predict/', data=data).json()["embedding"]
        dist, label = self.who_is_it(preds)

        out = {'label':label, 'dist':'{:.3f}'.format(dist)}

        return json.dumps(out)