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
        self.label_encoder = self.init_model("id2label.pkl")
    
    def init_model(self, model_name):
        """
        Initializes the machine learning model.

        Returns
        -------
        model: object
            Pre-trained model used
            to make predictions.
        """
        path = os.path.join(self.models_path, model_name)
        return pickle.load(open(path, 'rb'))

    def who_is_it(self, embed):
        """
        Performs the identity search 
        using the pre-trained knn model

        Parameters
        ----------
        embed: array
            Face embedding comming from the model.

        Returns
        -------
        dist: float
            distance between the given and 
            the target embedding.
        label: str
            Name of the predicted identity.
        """
        dist, label = self.model.kneighbors([embed])
        dist, label = dist[0,0], label[0,0]
        if dist > 1:
            label = "Unknown"
        else:
            label = self.label_encoder[label]
        return dist, label 

    def model_predict(self, data):
        """
        Decodes and preprocess the data, uses the 
        pretrained model to make predictions and 
        returns a well formatted json output.

        Parameters
        ----------
        data: bytes
            Base64 data comming from request.

        Returns
        -------
        outputs: json
            A json response that contains the output
            from the pre-trained model.
        """
        preds = requests.get(f'http://{self.vgg_host}/predict/', data=data).json()["embedding"]
        dist, label = self.who_is_it(preds)

        out = {'label':label, 'dist':'{:.3f}'.format(dist)}

        return json.dumps(out)