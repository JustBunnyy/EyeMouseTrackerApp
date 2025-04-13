import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import gradio as gr

# Init mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

# Get screen size
screen_w, screen_h = pyautogui.size()

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get left and right iris positions
            left_eye = face_landmarks.landmark[474]
            right_eye = face_landmarks.landmark[469]

            eye_x = int(left_eye.x * frame.shape[1])
            eye_y = int(left_eye.y * frame.shape[0])

            screen_x = screen_w * left_eye.x
            screen_y = screen_h * left_eye.y

            pyautogui.moveTo(screen_x, screen_y)

            # Optional: Draw circle on eyes
            cv2.circle(frame, (eye_x, eye_y), 10, (255, 0, 255), -1)

    return frame

# Gradio interface
demo = gr.Interface(
    fn=process_frame,
    inputs=gr.Image(source="webcam", streaming=True),
    outputs="image",
    live=True,
    title="AI Eye Mouse Tracker",
    description="Move your mouse using your eyes 👀 (Powered by MediaPipe + OpenCV)"
)

if __name__ == "__main__":
    demo.launch()
