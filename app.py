import json
from pathlib import Path

import streamlit as st

PROFILE_FILE = Path(__file__).parent / "snapDex.json"


@st.cache_data(ttl=60)
def load_profile():
    with open(PROFILE_FILE) as f:
        return json.load(f)["profile"]


st.set_page_config(page_title="Social Media Content Hub", page_icon="👻", layout="wide")

# --- SHARED PROFILE (snapDex.json) ---
profile = load_profile()
with st.sidebar:
    st.subheader(profile["name"])
    metrics = profile["metrics"]
    with st.container(horizontal=True):
        st.metric("Views", metrics["views"])
        st.metric("Likes", metrics["likes"])
    with st.container(horizontal=True):
        st.metric("Comments", metrics["comments"])
        st.metric("Shares", metrics["shares"])

# --- PAGE ROUTING ---
page = st.navigation([
    st.Page("app_pages/fan_connect.py", title="Fan connect", icon=":material/forum:", default=True),
    st.Page("app_pages/snapdex.py", title="SnapDex", icon=":material/contacts:"),
    st.Page("app_pages/lens_vault.py", title="Lens Vault", icon=":material/photo_filter:"),
])
page.run()
