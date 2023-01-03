from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import trackROI, InputException
from rq import Queue
from rq.job import Job
from worker import conn

q = Queue(connection=conn)
app = Flask(__name__)
CORS(app)

@app.route('/direct', methods=['POST'])
def post_direct():
    roi = request.form.get('roi')
    url = request.form.get('video')
    try:
        result = trackROI(url, roi)
        return jsonify(success=True, result=result)
    except InputException as err:
        return jsonify(success=False, message=err.message), 400

@app.route('/job', methods=['POST'])
def post_job():
    roi = request.form.get('roi')
    url = request.form.get('video')
    result = q.enqueue(trackROI, url, roi)
    return jsonify(success=True, job=result.id)

@app.route('/job/<job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.fetch(job_id, connection=conn)
    return jsonify(success=True, status=job.get_status(), result=job.result)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)