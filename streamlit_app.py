import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import threading
import av
import cv2
from eyetracker_module import EyeTracker

st.set_page_config(page_title="Eye Mouse Tracker", layout="centered")
st.title("🧠 Eye-Controlled Mouse & Emotion Tracker")

tracker = EyeTracker()

if 'tracking' not in st.session_state:
    st.session_state.tracking = False
if 'music_playing' not in st.session_state:
    st.session_state.music_playing = False

emotion_placeholder = st.empty()

class VideoProcessor(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        emotion = tracker.detect_emotion(img)
        if emotion:
            emotion_placeholder.markdown(f"**Current Emotion:** {emotion}")
        return img

st.subheader("🎥 Live Webcam Feed")
webrtc_streamer(key="eye-mouse", video_processor_factory=VideoProcessor)

col1, col2 = st.columns(2)

with col1:
    if not st.session_state.tracking:
        if st.button("▶️ Start Eye Tracking"):
            st.session_state.tracking = True
            threading.Thread(target=tracker.track_eyes, daemon=True).start()
    else:
        if st.button("⏹ Stop Eye Tracking"):
            tracker.stop()
            st.session_state.tracking = False

with col2:
    if not st.session_state.music_playing:
        if st.button("🎵 Play Music"):
            tracker.play_song()
            st.session_state.music_playing = True
    else:
        if st.button("🛑 Stop Music"):
            tracker.play_song("")
            st.session_state.music_playing = False

st.markdown("---")
st.caption("Built with ❤️ using Streamlit, MediaPipe, DeepFace, and PyAutoGUI")