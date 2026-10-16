from ultralytics import YOLO
from pathlib import Path

# --------------------------------
# 1. Dataset configuration
# --------------------------------

DATA_YAML = "data.yaml"

# --------------------------------
# 2. Load YOLO pretrained model
# --------------------------------

model = YOLO("yolo11n.pt")

# --------------------------------
# 3. Train model
# --------------------------------

results = model.train(
    data=DATA_YAML,
    epochs=30,
    imgsz=640,
    batch=8,
    name="cleancity_waste_model",
    project="models",
    patience=10
)

print("\nTraining completed successfully!")

# --------------------------------
# 4. Validate model
# --------------------------------

metrics = model.val()

print("\nModel Validation Completed")
print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)

# --------------------------------
# 5. Save best model
# --------------------------------

best_model = Path(
    "models/cleancity_waste_model/weights/best.pt"
)

if best_model.exists():
    print("\nBest model saved at:")
    print(best_model)
else:
    print("\nBest model file not found.")
