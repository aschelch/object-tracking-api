from os import abort
import cv2
from flask import jsonify

# tracker = cv2.TrackerCSRT_create()
tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()

class InputException(BaseException):
    def __init__(self, message):
        self.message = message

def trackROI(url, roi, start, end, rps = 5):

    video = cv2.VideoCapture(url)

    fps = round(video.get(cv2.CAP_PROP_FPS))
    totalNoFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = totalNoFrames / fps

    startFrame = round(start * fps)
    endFrame = round(end * fps)

    foo = round(fps/rps)

    print("roi:", roi)
    print("fps:", fps)
    print("rps:", rps)
    print("totalNoFrames:", totalNoFrames)
    print("durationInSeconds:", durationInSeconds, "s")

    print("startFrame:", startFrame, " endFrame:", endFrame)
    
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
    # data.append({
    #     "t": i*(1.0/fps),
    #     "x": int(bbox[0]), 
    #     "y": int(bbox[1]), 
    #     "w": int(bbox[2]), 
    #     "h": int(bbox[3])})

    i = -1
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        i+=1

        if i < startFrame:
            continue

        if endFrame <= i:
            break

        
        ok, bbox = tracker.update(frame)

        if (i % foo) != 0:
            continue

        data.append({
            "t": i*(1.0/fps),
            "x": int(bbox[0]), 
            "y": int(bbox[1]),
            "w": int(bbox[2]), 
            "h": int(bbox[3])})

    video.release()

    return data

