
from flask import Flask, Response, render_template_string
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__)

# Load your trained CleanCity AI model
MODEL_PATH = os.path.join(
    "runs", "detect", "models",
    "cleancity_waste_model-3", "weights", "best.pt"
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}. Check your model path."
    )

model = YOLO(MODEL_PATH)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CleanCity AI - Live Waste Detection</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f7f4;
            text-align: center;
            margin: 0;
            padding: 25px;
        }
        h1 { color: #218838; }
        .panel {
            max-width: 900px;
            margin: 20px auto;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px #0001;
        }
        img {
            width: 100%;
            max-width: 800px;
            border-radius: 10px;
        }
        .status { color: #555; }
    </style>
</head>
<body>
    <h1>🌿 CleanCity AI</h1>
    <p>Real-Time Waste Detection System</p>
    <div class="panel">
        <h2>Live Camera Feed</h2>
        <img src="/video_feed" alt="Live waste detection camera">
        <p class="status">
            Keep waste objects in front of your camera.
            Detection boxes and labels appear when recognized.
        </p>
    </div>
</body>
</html>
"""

def generate_frames():
    # Open the computer's default webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        camera.release()
        raise RuntimeError(
            "Camera not found. Check webcam permissions or try camera index 1."
        )

    try:
        while True:
            success, frame = camera.read()

            if not success:
                break

            # Run YOLO inference on the current frame
            results = model.predict(
                source=frame,
                conf=0.35,
                imgsz=640,
                verbose=False,
                device="cpu"
            )

            # Draw predicted boxes and labels
            annotated_frame = results[0].plot()

            # Encode the frame for browser streaming
            ok, buffer = cv2.imencode(".jpg", annotated_frame)

            if not ok:
                continue

            frame_bytes = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )
    finally:
        camera.release()


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False,
        threaded=True
    )
