from os import abort
import cv2
from flask import jsonify

tracker = cv2.TrackerCSRT_create()

class InputException(BaseException):
    def __init__(self, message):
        self.message = message

def trackROI(url, roi):

    video = cv2.VideoCapture(url)
    
    if not video.isOpened():
        raise InputException("Could not open video")

    ok, frame = video.read()
    if not ok:
        raise InputException("Could not open video")

    bbox = tuple(int(num) for num in roi.split(','))

    if len(bbox) != 4:
        raise InputException("Wrong ROI format. Expect : x,y,w,h")

    ok = tracker.init(frame, bbox)

    data = []
    data.append({"x": int(bbox[0]), "y": int(bbox[1]), "w": int(bbox[2]), "h": int(bbox[3])})

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        ok, bbox = tracker.update(frame)
        data.append({"x": int(bbox[0]), "y": int(bbox[1]),"w": int(bbox[2]), "h": int(bbox[3])})

    video.release()

    return data

