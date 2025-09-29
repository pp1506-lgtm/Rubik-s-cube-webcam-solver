from flask import Flask, render_template, request, jsonify, Response
import cv2
import os
import time

app = Flask(__name__)

# storage for captured face images
UPLOAD_FOLDER = 'static/captures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

faces = {}  # U, R, F, D, L, B

# initialize OpenCV webcam
camera = cv2.VideoCapture(0)  # 0 = default webcam

@app.route('/')
def index():
    return render_template('index.html')

# stream webcam video
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# capture a face from webcam
@app.route('/capture_face', methods=['POST'])
def capture_face():
    face = request.form.get('face')  # U, R, F, D, L, B
    if not face:
        return jsonify({"error": "Missing face label"}), 400

    success, frame = camera.read()
    if not success:
        return jsonify({"error": "Failed to capture image"}), 500

    filename = f"{face}_{int(time.time())}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(filepath, frame)

    faces[face] = filepath
    return jsonify({"status": "ok", "face": face, "url": f"/{filepath}"})

# solve once all faces are captured
@app.route('/solve', methods=['POST'])
def solve():
    required = ['U', 'R', 'F', 'D', 'L', 'B']
    missing = [f for f in required if f not in faces]

    if missing:
        return jsonify({"status": "error", "message": f"Missing faces: {missing}"}), 400

    # TODO: plug in OpenCV color detection + solver
    return jsonify({"status": "done", "solution": "R U R' U R U2 R'"})

if __name__ == '__main__':
    app.run(debug=True)
