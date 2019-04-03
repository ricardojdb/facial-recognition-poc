#!/usr/bin/env python
from datetime import datetime
from io import BytesIO
import numpy as np
import requests
import base64
import cv2
import os

from utils import utils
from utils import sql_utils

net = cv2.dnn.readNetFromCaffe("models/prototxt.txt", "models/res10_300x300_ssd_iter_140000.caffemodel")

sql_utils.create_mysql_table()
recog_dict = {}
# Start thread to capture and show the stream.
video_path = 0 
video_capture = utils.WebcamVideoStream(video_path).start()

host = "localhost"

while True:
    # Collect width and height from the stream
    h, w = int(video_capture.h), int(video_capture.w)
    # Read the current frame
    ret, frame = video_capture.read()

    if not ret:
        break
        
    img = np.copy(frame)
    
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
 
    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    net.setInput(blob)
    detections = net.forward()
    data = []
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            roi_color = frame[startY:endY, startX:endX]
            
            if not roi_color.size: continue
                
            roi_color_rgb = cv2.cvtColor(roi_color, cv2.COLOR_RGB2BGR)
            
            img_str = utils.encode_img(roi_color_rgb)

            r = requests.get(f'http://{host}:7000/predict/', data=img_str)

            outputs = dict(r.json())

            data.append([outputs['label'], outputs['dist'], (startX,startY,endX-startX,endY-startY)])
            
            if outputs['label'] == "Unknown": continue
                
            if outputs['label'] in recog_dict:
                recog_dict[outputs['label']][2] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            else:
                time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
                recog_dict[outputs['label']] = [outputs['label'], time, time]
            
  
    data_list = list(recog_dict.values())
    sql_utils.insert_mysql_table(data_list)
    
    video_capture.data_list = data
        
    if video_capture.stopped:
        break

cv2.destroyAllWindows()        