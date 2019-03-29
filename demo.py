#!/usr/bin/env python

from io import BytesIO
import numpy as np
import requests
import base64
import cv2
import os

from utils import utils

net = cv2.dnn.readNetFromCaffe("models/prototxt.txt", "models/res10_300x300_ssd_iter_140000.caffemodel")
host = "192.168.8.100"

cap = cv2.VideoCapture(0)
while 1:
    ret, frame = cap.read()
    
    if not ret:
        break
        
    img = np.copy(frame)
    (h, w) = frame.shape[:2]
    
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
 
    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    net.setInput(blob)
    detections = net.forward()
    
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.3:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            roi_color = frame[startY:endY, startX:endX]
            
            if not roi_color.size: continue
                
            roi_color_rgb = cv2.cvtColor(roi_color, cv2.COLOR_RGB2BGR)
            
            img_str = utils.encode_img(roi_color_rgb)

            r = requests.get(f'http://{host}:7000/predict/', data=img_str)

            r_dict = dict(r.json())

            img = utils.draw_box(img, r_dict['label'], r_dict['dist'], (startX,startY,endX-startX,endY-startY))  
    
    cv2.imshow('img',img)
    k = cv2.waitKey(32)
    if k & 0xFF == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()        