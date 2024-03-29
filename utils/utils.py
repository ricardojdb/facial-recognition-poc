from threading import Thread
from datetime import datetime

import win32com.client as wincl
import numpy as np

import traceback
import base64
import cv2
import sys
import os
import re


def speech2text_cortana(msg):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(msg)


def speak_name(name, firstSeen, lastSeen):
    first_seen = datetime.strptime(firstSeen, '%d/%m/%y %H:%M:%S')
    last_seen = datetime.strptime(lastSeen, '%d/%m/%y %H:%M:%S')

    difference = (last_seen-first_seen).seconds

    if difference < 20:
        # speak_cortana(name)
        msg = name + ", bienvenido"
        speech2text_cortana(msg)


def draw_box(img, label, dist, box):
    x, y, w, h = box
    box_color = (36, 174, 152)
    font_scale = 0.8
    thickness = 1
    font_type = cv2.FONT_HERSHEY_DUPLEX
    text = label  # + ' {:.3}'.format(dist)

    text_size = cv2.getTextSize(text, font_type, font_scale, thickness)[0]

    x_text = text_size[0] + int(text_size[0]*0.01)
    y_text = text_size[1] + int(text_size[1]*0.2)

    cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 2)

    if label != "Unknown":
        cv2.rectangle(img, (x, y), (x+x_text, y-y_text), box_color, 8)
        cv2.rectangle(img, (x, y), (x+x_text, y-y_text), box_color, -1)

        cv2.putText(img, text, (x, y), font_type, font_scale,
                    (255, 255, 255), thickness)

    return img


def get_wide_box(w, h, xmin, ymin, xmax, ymax):
    """
    Expands the boundary face box
    """
    xmin_wide = max(xmin-(xmax-xmin)//4, 0)
    ymin_wide = max(ymin-(ymax-ymin)//4, 0)
    xmax_wide = min(xmax+(xmax-xmin)//6, w-1)
    ymax_wide = min(ymax+(ymax-ymin)//6, h-1)
    return xmin_wide, ymin_wide, xmax_wide, ymax_wide


def encode_img(img):
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)
    return img_str


def get_photos(base_path):
    photos = {}

    for path in os.listdir(base_path):
        if path.endswith("jpg") or \
           path.endswith("png") or \
           path.endswith("jpeg"):
            image_path = os.path.join(base_path, path)
            encoded_image = base64.b64encode(
                open(image_path, 'rb').read()).decode('utf-8')
            name = re.sub("[0-9]", "", path[:-4])
            photos[name] = encoded_image

    return photos


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and
        # read the first frame from the stream
        self.stream = cv2.VideoCapture(src)
        # Change depending on the resolution of the camera
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 1280
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 720
        self.stream.set(cv2.CAP_PROP_FPS, 60)  # 720

        self.h = self.stream.get(4)
        self.w = self.stream.get(3)
        (self.grabbed, self.frame) = self.stream.read()

        self.data_list = []
        # initialize the variable used to indicate
        # if the thread should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        self.stopped = False
        self.thread = Thread(target=self.update, name='camera:0', args=())
        self.thread.start()
        return self

    def update(self):
        cv2.namedWindow('final_image', cv2.WINDOW_NORMAL)
        # cv2.namedWindow('final_image', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(
        # "final_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # keep looping infinitely until the thread is stopped
        while True:
            try:
                # if the thread indicator variable is set, stop the thread
                if self.stopped:
                    self.stream.release()
                    cv2.destroyAllWindows()
                    return

                # otherwise, read the next frame from the stream
                (self.grabbed, self.frame) = self.stream.read()
                self.h = self.stream.get(4)
                self.w = self.stream.get(3)
                img = np.copy(self.frame)

                if not self.grabbed:
                    print('No frames')
                    self.stop()
                    self.stream.release()
                    cv2.destroyAllWindows()
                    return

                if len(self.data_list) > 0:
                    for data in self.data_list:
                        img = draw_box(img, data[0], data[1], data[2])

                cv2.imshow('final_image', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stream.release()
                    cv2.destroyAllWindows()
                    self.stop()
                    return

            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                return

    def read(self):
        # return the frame most recently read
        return (self.grabbed, self.frame)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
