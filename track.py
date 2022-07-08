from flask import Flask, request, jsonify
import cv2
import sys

app = Flask(__name__)

tracker = cv2.TrackerCSRT_create()

@app.route('/track', methods=['POST'])
def post_something():
    roi = request.form.get('roi')
    url = request.form.get('video')

    print(f"ROI: {roi}")
    print(f"Video: {url}")

    response = {}

    video = cv2.VideoCapture(url)
   
    if not video.isOpened():
        response["ERROR"] = "Could not open video"
        return jsonify(response)

    ok, frame = video.read()
    if not ok:
        response["ERROR"] = "Cannot read video file"
        return jsonify(response)

    bbox = tuple(int(num) for num in roi.split(','))


    print(f"Processing...")

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    response["DATA"] = []
    response["DATA"].append({
           "x": int(bbox[0]), "y": int(bbox[1]),
           "h": int(bbox[2]), "w": int(bbox[3])
    })

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        ok, bbox = tracker.update(frame)
        response["DATA"].append({
           "x": int(bbox[0]), "y": int(bbox[1]),
           "h": int(bbox[2]), "w": int(bbox[3])
        })

    video.release()

    # Return the response in json format
    return jsonify(response)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)