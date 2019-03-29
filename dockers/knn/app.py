from flask import Flask, request
import numpy as np

import utils

app = Flask(__name__)

knn = utils.KnnModel("models/", "172.17.0.2:7000")

@app.route('/predict/',methods=['GET','POST'])
def predict():

	data = request.get_data()
	output = knn.model_predict(data)

	return output	

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=7000)