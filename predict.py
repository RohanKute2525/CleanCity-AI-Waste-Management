from ultralytics import YOLO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Trained model
MODEL_PATH = (
    BASE_DIR
    / "runs"
    / "detect"
    / "models"
    / "cleancity_waste_model-3"
    / "weights"
    / "best.pt"
)

# Test folder
TEST_DIR = BASE_DIR / "dataset" / "images" / "test"

print("===================================")
print("       CleanCity AI Prediction")
print("===================================")

print("Model:", MODEL_PATH)

# Check model
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# Find test images automatically
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]

test_images = []

for extension in image_extensions:
    test_images.extend(TEST_DIR.glob(extension))

if not test_images:
    raise FileNotFoundError(
        f"No test images found in: {TEST_DIR}"
    )

# Select first image
IMAGE_PATH = test_images[0]

print("Test Image:", IMAGE_PATH)

# Load model
print("\nLoading trained model...")
model = YOLO(str(MODEL_PATH))

# Prediction
print("Running prediction...\n")

results = model.predict(
    source=str(IMAGE_PATH),
    conf=0.25,
    save=True
)

# Display results
for result in results:

    print("========== DETECTION RESULT ==========")

    if result.boxes is None or len(result.boxes) == 0:
        print("No waste detected.")
        continue

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = result.names[class_id]

        print(f"Waste Type : {class_name}")
        print(f"Confidence : {confidence * 100:.2f}%")
        print("--------------------------------------")

print("\nPrediction completed successfully!")

print(
    "\nOutput saved in:",
    BASE_DIR / "runs" / "detect" / "predict"
)
