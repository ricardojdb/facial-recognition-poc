import numpy as np
import base64
import cv2

def draw_box(img, label, dist, box):
    x,y,w,h = box
    
    font_scale = 0.8
    thickness = 1
    font_type = cv2.FONT_HERSHEY_DUPLEX
    text = label + ' {:.3}'.format(dist)
    
    text_size = cv2.getTextSize(text, font_type, font_scale, thickness)[0]
    
    x_text = text_size[0] + int(text_size[0]*0.01)
    y_text = text_size[1] + int(text_size[1]*0.2)
    
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 5)
    cv2.rectangle(img, (x,y), (x+x_text, y-y_text), (255,0,0), 5)
    cv2.rectangle(img, (x,y), (x+x_text, y-y_text), (255,0,0), -1)

    cv2.putText(img, text, (x,y), font_type, font_scale, (255,255,255), thickness)
    
    return img

def encode_img(img):
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)
    return img_str