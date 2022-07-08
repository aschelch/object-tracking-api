from flask import Flask, request, jsonify
import cv2
import sys

app = Flask(__name__)

tracker = cv2.TrackerCSRT_create()


@app.route('/track/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /track/?roi=
    roi = request.args.get("roi", None)
    print(f"Received: {roi}")

    response = {}

    video = cv2.VideoCapture("poc/street.mp4")
   
    if not video.isOpened():
        response["ERROR"] = "Could not open video"
        return jsonify(response)

    ok, frame = video.read()
    if not ok:
        response["ERROR"] = "Cannot read video file"
        return jsonify(response)

    bbox = tuple(int(num) for num in roi.split(','))

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    response["DATA"] = []

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


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome API!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)