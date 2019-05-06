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

net = cv2.dnn.readNetFromCaffe( 
    "models/prototxt.txt", 
    "models/res10_300x300_ssd_iter_140000.caffemodel")

sql_utils.create_mysql_table()
sql_utils.delete_mysql_table()

recog_dict = {}
# Start thread to capture and show the stream.
video_path = 0
video_capture = utils.WebcamVideoStream(video_path).start()

host = "localhost"

while True:
    # collect width and height from the stream
    h, w = int(video_capture.h), int(video_capture.w)
    
    # read the current frame
    ret, frame = video_capture.read()

    if not ret:
        break
        
    img = np.copy(frame)
    
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, 
        (300, 300), (104.0, 177.0, 123.0))
 
    # apply OpenCV's face detector in the input image
    net.setInput(blob)
    detections = net.forward()
    data = []

    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # compute the (x, y)-coordinates of the bounding box 
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (xmin, ymin, xmax, ymax) = box.astype("int")
            # Widen the box so we can capture the whole face
            xmin_wide, ymin_wide, xmax_wide, ymax_wide = utils.get_wide_box(
                w, h, xmin, ymin, xmax, ymax)

            # cut face from the frame
            roi_color = frame[ymin_wide:ymax_wide, xmin_wide:xmax_wide]

            # if no face is detected conitnue to the next one
            if not roi_color.size: continue

            # encode image to base64
            img_str = utils.encode_img(roi_color)

            # send the image in the data param
            r = requests.get(f'http://{host}:7000/predict/', params={"data":img_str})

            # extract json output
            outputs = dict(r.json())

            # gather the data that's going to be passed to
            # the WebcamVideoStream to plot the bounding box
            data.append([outputs['label'], outputs['dist'], (xmin,ymin,xmax-xmin,ymax-ymin)])
            
            # if label is Unknown don't add the data to the MySQL database
            if outputs['label'] == "Unknown": continue
            
            # create or update the data in the recognition dict
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