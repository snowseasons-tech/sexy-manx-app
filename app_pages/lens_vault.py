from pathlib import Path

import streamlit as st

st.iframe(Path(__file__).resolve().parent.parent / "lens_vault.html", height=1000, alt="Lens Vault AR filter studio")
