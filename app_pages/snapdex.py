from pathlib import Path

import streamlit as st

st.iframe(Path(__file__).resolve().parent.parent / "snapchat_contact_streak_manager.html", height=1000, alt="SnapDex contact and streak manager")
