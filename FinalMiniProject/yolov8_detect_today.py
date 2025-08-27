
from ultralytics import YOLO
import os
import csv
from datetime import datetime

model = YOLO('yolov8n.pt')
image_folder = "mold_images"

# CSV Logging
log_file = "detection_log.csv"
log_exists = os.path.isfile(log_file)
logfile = open(log_file, mode="a", newline="", encoding="utf-8")
log_writer = csv.writer(logfile)
if not log_exists:
    log_writer.writerow(["Image", "Prediction", "Confidence", "Timestamp"])

today = datetime.now().strftime("%Y%m%d")
for filename in os.listdir(image_folder):
    if today in filename and (filename.endswith('.jpg') or filename.endswith('.png')):
        img_path = os.path.join(image_folder, filename)
        results = model(img_path, conf=0.25)

        prediction = "Mold Detected" if "mold" in filename.lower() else "Clean"
        if results[0].boxes and results[0].boxes.conf.numel() > 0:
            confidence = round(float(results[0].boxes.conf[0]) * 100, 2)
        else:
            confidence = 0.0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n Processing: {filename}")
        print(f"Prediction: {prediction} | Confidence: {confidence}%")

        results[0].show()
        results[0].save(filename=f"detected_{filename}")
        log_writer.writerow([filename, prediction, confidence, timestamp])
logfile.close()
