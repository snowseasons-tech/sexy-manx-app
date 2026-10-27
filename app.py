import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION & DATABASE SETUP ---
DB_FILE = "questions_db.json"
PASSWORD = "snowbrooks"  # Change this to a secure password for your wife

# Simple JSON file database helper functions
def load_questions():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_questions(questions):
    with open(DB_FILE, "w") as f:
        json.dump(questions, f, indent=4)

# --- IMAGE GENERATOR FUNCTION ---
def generate_snap_card(fan_name, question_text):
    # Standard high-res Snapchat story aspect ratio (1080x1920)
    img = Image.new("RGB", (1080, 1920), color="#111111") # Sleek AMOLED Dark Background
    draw = ImageDraw.Draw(img)

    # Try to load clean modern fonts, fallback to default if not installed
    try:
        font_handle = ImageFont.truetype("Arial.ttf", 40)
        font_body = ImageFont.truetype("Arial.ttf", 55)
        font_footer = ImageFont.truetype("Arial.ttf", 36)
    except IOError:
        font_handle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # --- 1. Draw the Main Content Card ---
    # Centered card coordinates
    card_x1, card_y1, card_x2, card_y2 = 100, 600, 980, 1250
    draw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=45,
        fill="#FFFFFF",
        outline="#FFFC00", # Snapchat Yellow border accent
        width=6
    )

    # --- 2. Draw Fan Handle Header ---
    display_name = f"@{fan_name.strip().replace('@', '')}" if fan_name.lower() != 'anonymous' else "Anonymous Fan"
    draw.text((160, 660), display_name, fill="#888888", font=font_handle)

    # --- 3. Advanced Word Wrapping for the Question ---
    words = question_text.split()
    lines = []
    current_line = ""

    # Dynamically wrap text based on character width restrictions
    for word in words:
        test_line = f"{current_line} {word}".strip()
        # Roughly 26 characters max per line for font size 55 inside this card width
        if len(test_line) <= 26:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Render text lines down the card with clean line height spacing
    y_offset = 760
    max_visible_lines = 5
    for line in lines[:max_visible_lines]:
        draw.text((160, y_offset), line, fill="#111111", font=font_body)
        y_offset += 80  # Line spacing

    # --- 4. Call-to-Action Footer ---
    # Add a glowing text indicator at the bottom of the card to encourage story engagement
    draw.text((540, 1170), "TAP TO REPLY 💬", fill="#FFFC00", font=font_footer, anchor="ms")

    # Save image temporarily
    output_path = "snap_story_card.png"
    img.save(output_path)
    return output_path
# --- UI APP ROUTING ---
st.set_page_config(page_title="Snapchat Fan Connect", page_icon="👻", layout="centered")

# Multi-tab view: one for fans to submit, one private for your wife
tab_fan, tab_creator = st.tabs(["📣 Ask Me Anything (Fan View)", "🔒 Creator Dashboard"])

# 1. FAN VIEW
with tab_fan:
    st.title("👻 Send Me a Question!")
    st.write("Fill out the form below to submit a question, dare, or shoutout request for my next Snapchat Story!")
    
    with st.form("submission_form", clear_on_submit=True):
        fan_name = st.text_input("Your Name / Snapchat Handle", placeholder="Anonymous")
        question_text = st.text_area("Your Question", placeholder="What do you want to ask?", max_chars=280)
        submit_btn = st.form_submit_button("Send to Story Queue ✨")
        
        if submit_btn:
            if not question_text.strip():
                st.error("Please type a question before sending!")
            else:
                questions = load_questions()
                new_q = {
                    "id": len(questions) + 1,
                    "fan_name": fan_name.strip() if fan_name.strip() else "Anonymous",
                    "question_text": question_text.strip(),
                    "status": "pending",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                }
                questions.append(new_q)
                save_questions(questions)
                st.success("Sent! Keep an eye on my Snapchat stories to see if I pick yours! 🎉")

# 2. CREATOR DASHBOARD (Your Wife's Backstage Area)
with tab_creator:
    st.title("👑 Your Backstage Center")
    access_password = st.text_input("Enter Access Password", type="password")
    
    if access_password == PASSWORD:
        st.success("Access Granted.")
        questions = load_questions()
        pending_qs = [q for q in questions if q["status"] == "pending"]
        
        st.subheader(f"📥 Pending Questions ({len(pending_qs)})")
        
        if not pending_qs:
            st.info("No questions in the queue yet. Share your public link with your fans!")
        
        for q in pending_qs:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**From:** {q['fan_name']} *({q['timestamp']})*")
                    st.write(f"\"{q['question_text']}\"")
                with col2:
                    # When she clicks this, it auto-generates the customized png layout
                    if st.button("Generate Card 🎨", key=f"gen_{q['id']}"):
                        card_path = generate_snap_card(q['fan_name'], q['question_text'])
                        
                        # Show a small preview in the dashboard
                        st.image(card_path, caption="Your Snapchat Story Preview", width=200)
                        
                        # Provide a download button for her mobile phone or desktop
                        with open(card_path, "rb") as file:
                            st.download_button(
                                label="Download Image 📥",
                                data=file,
                                file_name=f"snap_card_{q['id']}.png",
                                mime="image/png",
                                key=f"dl_{q['id']}"
                            )
                st.markdown("---")
    elif access_password:
        st.error("Incorrect password. Please try again.")
