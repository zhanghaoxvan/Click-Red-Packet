try:
    import pyautogui, cv2, numpy as np, time
except ModuleNotFoundError:
    print("Module not found. Pls check your .venv environment.")
    print("Click the Docs of Python Website: https://docs.python.org/3/library/venv.html#how-venvs-work for more information.")
    exit(1)

RED_PACKET_COLOR_INIT = (225, 141, 53)
RED_PACKET_COLOR_CLICKED = (175, 110, 41)
OPEN_COLOR = (235, 205, 154)
COLOR_TOLERANCE = 10
SCREEN_REGION = None
CLICK_DELAY = 0.1
SCAN_INTERVAL = 0.1

def captureScreen(region=SCREEN_REGION):
    screenshot = pyautogui.screenshot(region=region)
    frame = cv2.cvtColor(np.array(screenshot).copy(), cv2.COLOR_RGB2BGR)
    return frame

def findColorInScreen(frame, target_color, tolerance, region=SCREEN_REGION):
    lower = np.array([max(0, c - tolerance) for c in target_color])
    upper = np.array([min(255, c + tolerance) for c in target_color])
    mask = cv2.inRange(frame, lower, upper)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) < 50:
            return None
        M = cv2.moments(largest_contour)
        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if region:
                cX += region[0]
                cY += region[1]
            print(f"Detected target color! Position: ({cX}, {cY})")
            return cX, cY
    return None

def autoClick():
    try:
        print("The Click-Red-Packet Batch will start in 3 seconds...")
        print("Press Ctrl+C(Windows/Linux) or ⌃C(MacOS) to Stop the Batch")
        time.sleep(3)
        pyautogui.PAUSE = 0.05
        while True:
            frame = captureScreen()
            position = findColorInScreen(frame, RED_PACKET_COLOR_INIT, COLOR_TOLERANCE)
            if position:
                x, y = position
                pyautogui.moveTo(x, y, duration=0.05)
                pyautogui.click(x, y)
                print(f"Clicked Red Packet! Position: ({x}, {y})")
                time.sleep(CLICK_DELAY)
                continue
            # print("Found nothing. Waiting for the next pocket...")
            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\nBatch stopped manually by pressing Ctrl+C or ⌃C")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    autoClick()
