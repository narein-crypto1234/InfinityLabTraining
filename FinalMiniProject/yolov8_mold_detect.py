from ultralytics import YOLO
import cv2
import os
import csv
from datetime import datetime

# Load a pretrained YOLOv8 model
model = YOLO('yolov8n.pt')
image_folder = "mold_images/"

# CSV Logging
log_file = "detection_log.csv"
log_exists = os.path.isfile(log_file)
logfile = open(log_file, mode="a", newline="")
log_writer = csv.writer(logfile)

if not log_exists:
    log_writer.writerow(["Image", "Prediction", "Confidence", "Timestamp"])

# Loop through each image
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        img_path = os.path.join(image_folder, filename)
        results = model(img_path, conf=0.25)

        # Simulated prediction
        prediction = " Mold Detected" if "mold" in filename.lower() else "Clean"

        # Safe confidence fallback
        if results[0].boxes and results[0].boxes.conf.numel() > 0:
            confidence = round(float(results[0].boxes.conf[0]) * 100, 2)
        else:
            confidence = 0.0

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Show result
        print(f"\n Processing: {filename}")
        print(f"Simulated prediction for: {filename}")
        print(f"Confidence: {confidence}%")
        print(f"Final Result: {prediction}")

        # Save annotated image
        results[0].show()
        results[0].save(filename=f"detected_{filename}")

        # Log to CSV
        log_writer.writerow([filename, prediction, confidence, timestamp])

logfile.close()
