import cv2
from datetime import datetime

# Start the webcam (0 = default camera)
cap = cv2.VideoCapture(0)
print("📸 Press SPACE to capture, ESC to exit")

while True:
    ret, frame = cap.read()
    cv2.imshow("Live Camera", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break
    elif key == 32:  # SPACE key
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mold_images/captured_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ Image saved: {filename}")

cap.release()
cv2.destroyAllWindows()
