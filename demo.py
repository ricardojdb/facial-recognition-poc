#!/usr/bin/env python
from datetime import datetime
from io import BytesIO

import pandas as pd
import numpy as np

import threading
import requests
import base64
import utils
import cv2
import os

from utils import sql_utils

# SQL data
sql_utils.create_mysql_table()
sql_utils.delete_mysql_table()

recog_dict = {}
# Start thread to capture and show the stream.
video_path = 0
video_capture = utils.WebcamVideoStream(video_path).start()

host = "localhost"

spoken_names = set()

while True:
    # collect width and height from the stream
    h, w = int(video_capture.h), int(video_capture.w)

    # read the current frame
    ret, frame = video_capture.read()

    if not ret:
        break

    img = np.copy(frame)

    # Call Face detection API
    try:
        detect_req = requests.post(
            url=f'http://{host}:7000/predict/',
            data=utils.encode_img(img),
            timeout=5)
        detections = detect_req.json()
    except:
        detections = []

    data = []
    for face in detections:
        # extract the confidence associated with the prediction
        confidence = face["confidence"]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.3:
            # compute the (x, y)-coordinates of the bounding box for the object
            box = face["box"] * np.array([w, h, w, h])
            (xmin, ymin, xmax, ymax) = box.astype("int")

            # Widen the box so we can capture the whole face
            xmin_wide, ymin_wide, xmax_wide, ymax_wide = utils.get_wide_box(
                w, h, xmin, ymin, xmax, ymax)

            # cut face from the frame
            roi_color = frame[ymin_wide:ymax_wide, xmin_wide:xmax_wide]

            # if no face is detected conitnue to the next one
            if not roi_color.size:
                continue

            # encode image to base64
            img_str = utils.encode_img(roi_color)

            # send the image in the data param
            r = requests.post(
                url=f'http://{host}:7002/predict/',
                params={"data": img_str})

            # extract json output
            outputs = dict(r.json())

            # gather the data that's going to be passed to
            # the WebcamVideoStream to plot the bounding box
            data.append([
                outputs['label'],
                outputs['dist'],
                (xmin, ymin, xmax-xmin, ymax-ymin)])

            # if label is Unknown don't add the data to the MySQL database
            if outputs['label'] == "Unknown":
                continue

            # create or update the data in the recognition dict
            if outputs['label'] in recog_dict:
                last_seen = datetime.now().strftime('%d/%m/%y %H:%M:%S')
                recog_dict[outputs['label']][2] = last_seen
                sql_utils.update_mysql_table(outputs['label'], last_seen)
            else:
                time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
                recog_dict[outputs['label']] = [outputs['label'], time, time]
                sql_utils.insert_mysql_table(recog_dict[outputs['label']])

            if outputs['label'] not in spoken_names:
                processThread = threading.Thread(
                    target=utils.speak_name,
                    args=(outputs['label'],
                          recog_dict[outputs['label']][1],
                          recog_dict[outputs['label']][2]))

                processThread.start()
                spoken_names.add(outputs['label'])

    video_capture.data_list = data

    if video_capture.stopped:
        break

cv2.destroyAllWindows()
