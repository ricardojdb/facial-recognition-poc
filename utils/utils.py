from threading import Thread

import numpy as np
import traceback
import base64
import cv2
import sys
import os 

global logos

logos = [cv2.imread("C:\\Users\\rdiazbri\\Documents\\proyectos\\facial-recognition-poc\\logos\\everis.png")]
name2logo = {"Ricardo Diaz": 0, 
             "Jose Sosa": 0, 
             "Hugo Castro": 0, 
             "Jaspers": 0}

def draw_logo(img, label, logo_x, logo_y, logo_w, logo_h):
    logo_id = name2logo.get(label, None)
    if logo_id is None:
        return img
    logo = logos[logo_id]
    if logo is None:
        return img
    logo = cv2.resize(logo, (logo_w , logo_h))

    logo_gray = cv2.cvtColor(logo,cv2.COLOR_BGR2GRAY)
    mask = (logo_gray<100)

    logo_ymin = int(logo_y+2)
    logo_xmin = int(logo_x-5)
    true_h,true_w, _ = img[logo_ymin:logo_ymin+logo_h, logo_xmin:logo_xmin+logo_w].shape
    img[logo_ymin:logo_ymin+logo_h, logo_xmin:logo_xmin+logo_w] *= np.expand_dims(mask[:true_h,:true_w],-1)
    img[logo_ymin:logo_ymin+logo_h, logo_xmin:logo_xmin+logo_w] += logo[:true_h,:true_w]

    return img

def draw_box(img, label, dist, box):
    x,y,w,h = box
    box_color = (36, 174, 152)
    font_scale = 0.8
    thickness = 1
    font_type = cv2.FONT_HERSHEY_DUPLEX
    text = label #+ ' {:.3}'.format(dist)
    
    text_size = cv2.getTextSize(text, font_type, font_scale, thickness)[0]
    
    x_text = text_size[0] + int(text_size[0]*0.01)
    y_text = text_size[1] + int(text_size[1]*0.2)
    
    cv2.rectangle(img, (x,y), (x+w,y+h), box_color, 2)

    if label != "Unknown":
        cv2.rectangle(img, (x,y), (x+x_text, y-y_text), box_color, 8)
        cv2.rectangle(img, (x,y), (x+x_text, y-y_text), box_color, -1)

        cv2.putText(img, text, (x,y), font_type, font_scale, (255,255,255), thickness)
        # cv2.putText(img, text, (x,y), font_type, font_scale, (255,255,255), 1)
        img = draw_logo(img, label, x+x_text+15, y-y_text-10, 60, 41)
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
        if path.endswith("jpg") or path.endswith("png") or path.endswith("jpeg"):
            image_path = os.path.join(base_path, path)
            encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')
            photos[path[:-4]] = encoded_image
            
    return photos

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame from the stream
        self.stream = cv2.VideoCapture(src)
        # Change depending on the resolution of the camera
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.h = self.stream.get(4)
        self.w =self.stream.get(3)
        (self.grabbed, self.frame) = self.stream.read()

        self.data_list = None
        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        self.stopped = False
        self.thread = Thread(target=self.update, name='camera:0', args=())
        self.thread.start()
        return self
 
    def update(self):
        cv2.namedWindow('final_image', cv2.WINDOW_NORMAL)
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
                self.w =self.stream.get(3)
                img = np.copy(self.frame)
                
                if not self.grabbed:
                    print('No frames')
                    self.stop()
                    self.stream.release()
                    cv2.destroyAllWindows()
                    return

                if self.data_list != None:
                    for data in self.data_list:                        
                        img = draw_box(img, data[0], data[1], data[2])

                cv2.imshow('final_image',img)
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