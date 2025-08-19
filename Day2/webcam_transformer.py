import cv2
import numpy as np
from datetime import datetime
import os


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def hud(img, text):
    out = img.copy()

    if out.ndim == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)

    cv2.rectangle(out, (0, 0), (out.shape[1], 28), (0, 0, 0), -1)

    # Corrected line: 'text' is a string, so it should be used directly
    cv2.putText(out, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    return out

def mode_name(m):
    names = {
        0: "original",
        1: "Grayscale",
        2: "Gaussian Blur",
        3: "Median Blur",
        4: "Canny Edges",
        5: "Sobel Magnitude",
        6: "Sharpen",
    }
    return names.get(m, "Original")


# Core image processing function (consolidated)
def apply_transform(mode, frame_bgr):
    # Fallback to original if unknown mode
    processed_img = frame_bgr
    
    if mode == 0:
        # Original (color)
        processed_img = frame_bgr
    elif mode == 1: 
        # Grayscale
        g = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        processed_img = g
    elif mode == 2:
        # Gaussian Blur (applied on grayscale)
        g = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        gb = cv2.GaussianBlur(g, (7, 7), 1.4)
        processed_img = gb
    elif mode == 3:
        # Median Blur (applied on grayscale)
        g = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        mb = cv2.medianBlur(g, 5)
        processed_img = mb
    elif mode == 4: 
        # Canny Edge (applied on grayscale)
        g = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(g, 80, 160)
        processed_img = edges
    elif mode == 5:
        # Sobel gradient magnitude (grayscale)
        g = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
        sy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(sx, sy)
        mmax = float(np.max(mag)) if mag.size else 0.0
        if mmax > 1e-6:
            mag = (mag / mmax) * 255.0
        processed_img = np.clip(mag, 0, 255).astype(np.uint8)
    elif mode == 6: 
        # Sharpen (on color)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        shp = cv2.filter2D(frame_bgr, -1, kernel)
        processed_img = shp
        
    return processed_img, processed_img


# Main 100p: open webcam, process frames, display & handle keys

def main(cam_index=0, width=1280, height=720):
    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if not cap.isOpened():
        print("Error: Cannot open webcam. Try cam_index=1 (USB cam) or close apps using the camera.")
        return
    try:
        os.makedirs("captures", exist_ok=True)
    except Exception as e:
        print("Warning: cannot create captures folder:", e)
    
    print("""
    Controls:
    0: Original
    1: Grayscale
    2: Gaussian Blur
    3: Median Blur
    4: Canny
    5: Sobel Magnitude
    6: Sharpen
    c: Capture processed frame to ./captures/
    q: Quit
    """)

    mode = 1
    win = "Webcam Mini (press 0..6 to change mode)"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Warning: failed to read frame.")
                continue

            processed, save_img = apply_transform(mode, frame)
            
            # Corrected formatting for HUD text
            txt = f"{mode_name(mode)} | keys: 0-6=modes, c=capture, q=quit"
            disp = hud(processed, txt)

            if disp.ndim == 2:
                disp_bgr = cv2.cvtColor(disp, cv2.COLOR_GRAY2BGR)
            else:
                disp_bgr = disp

            cv2.imshow(win, disp_bgr)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            elif k == ord('c'):
                # Corrected filename string formatting
                fname = f"captures/{timestamp()}_{mode_name(mode).replace(' ', '_')}.png"
                cv2.imwrite(fname, save_img)
                print("Saved:", fname)
            elif k in [ord(str(i)) for i in range(7)]:
                mode = int(chr(k))
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main(cam_index=0, width=1280, height=720)