"""
Experimental hand-gesture controller.

Requires:
    pip install mediapipe opencv-python pyautogui

This keeps mappings intentionally simple:
- Open palm -> play/pause
- Index finger raised -> scroll up
- Two fingers raised -> scroll down

Run this module separately while testing so camera automation cannot surprise you.
"""

def run_gesture_loop(camera_index=0):
    try:
        import cv2
        import mediapipe as mp
        import pyautogui
    except ImportError:
        print("Gesture dependencies are not installed.")
        return

    hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(camera_index)

    print("Gesture mode active. Press Q in the camera window to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            lm = hand.landmark

            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y
            ring_up = lm[16].y < lm[14].y
            pinky_up = lm[20].y < lm[18].y

            raised = sum([index_up, middle_up, ring_up, pinky_up])

            if raised >= 4:
                pyautogui.press("playpause")
            elif index_up and not middle_up:
                pyautogui.scroll(3)
            elif index_up and middle_up and not ring_up:
                pyautogui.scroll(-3)

            draw.draw_landmarks(
                frame,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS,
            )

        cv2.imshow("Soku Gestures", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    run_gesture_loop()
