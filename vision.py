"""
Optional local camera perception.

This module intentionally avoids claiming to know a person's internal emotional
state. It can detect whether a face is present and provide a rough visual cue
based on simple image measurements.
"""

def inspect_camera_once(camera_index=0):
    try:
        import cv2
    except ImportError:
        return {
            "ok": False,
            "message": "OpenCV is not installed.",
        }

    cap = cv2.VideoCapture(camera_index)
    ok, frame = cap.read()
    cap.release()

    if not ok:
        return {"ok": False, "message": "I couldn't access the camera."}

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return {
            "ok": True,
            "face_present": False,
            "message": "I don't see a face right now.",
        }

    # Deliberately conservative: presence only, not emotion diagnosis.
    return {
        "ok": True,
        "face_present": True,
        "message": "I can see you. How are you doing?",
    }
