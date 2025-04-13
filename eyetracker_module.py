import cv2
import mediapipe as mp
import pyautogui
from deepface import DeepFace
import threading
import pygame

class EyeTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.cam = cv2.VideoCapture(0)
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False
        self.running = False
        self.music_playing = False
        pygame.mixer.init()

    def play_song(self, song_path="happy_song.mp3"):
        if song_path:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.music_playing = True
        else:
            pygame.mixer.music.stop()
            self.music_playing = False

    def detect_emotion(self, image):
        try:
            result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            return result[0]['dominant_emotion']
        except Exception as e:
            print("Emotion detection error:", e)
            return None

    def track_eyes(self):
        self.running = True
        while self.running:
            ret, image = self.cam.read()
            if not ret:
                break
            image = cv2.flip(image, 1)
            window_h, window_w, _ = image.shape
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            processed_image = self.face_mesh.process(rgb_image)
            landmarks = processed_image.multi_face_landmarks
            if landmarks:
                face_landmarks = landmarks[0].landmark
                for id, landmark in enumerate(face_landmarks[474:478]):
                    x = int(landmark.x * window_w)
                    y = int(landmark.y * window_h)
                    if id == 1:
                        speed_factor = 1.5
                        mouse_x = int(self.screen_w / window_w * x * speed_factor)
                        mouse_y = int(self.screen_h / window_h * y * speed_factor)
                        pyautogui.moveTo(mouse_x, mouse_y)
        self.cam.release()

    def stop(self):
        self.running = False
        self.play_song("")  # Stop music if playing

if __name__ == "__main__":
    tracker = EyeTracker()
    threading.Thread(target=tracker.track_eyes).start()