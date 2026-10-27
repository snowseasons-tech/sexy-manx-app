import streamlit as st
import html
import json
import os
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION & DATABASE SETUP ---
DB_FILE = "questions_db.json"
PASSWORD = "snowbrooks"  # Secure password for your wife

THEMES = {
    "🌸 Pastel Pink Dream": {
        "bg": "#FFF0F5", "card": "#FFFFFF", "border": "#FFB6C1",
        "text_main": "#4A2E35", "text_mute": "#9E7B83", "accent": "#FF69B4"
    },
    "⚡ Neon Cyberpunk": {
        "bg": "#0D0E15", "card": "#1A1C28", "border": "#00FFFF",
        "text_main": "#FFFFFF", "text_mute": "#6272A4", "accent": "#FF79C6"
    },
    "☁️ Minimalist White": {
        "bg": "#F9F9FB", "card": "#FFFFFF", "border": "#E2E8F0",
        "text_main": "#0F172A", "text_mute": "#64748B", "accent": "#000000"
    }
}

# Safely read data without losing thread safety
def read_json_file():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        with open(DB_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

# Thread-safe write utility
def write_json_file(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Streamlit-safe state management wrapper
def load_questions():
    if "questions_list" not in st.session_state:
        st.session_state.questions_list = read_json_file()
    return st.session_state.questions_list

def save_questions(questions):
    st.session_state.questions_list = questions
    write_json_file(questions)

# --- IMAGE GENERATOR FUNCTION ---
def generate_snap_card(fan_name, question_text, theme_name, answer_text=""):
    t = THEMES[theme_name]
    img = Image.new("RGB", (1080, 1920), color=t["bg"])
    draw = ImageDraw.Draw(img)

    def load_font(size):
        for name in ("Arial.ttf", "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except IOError:
                continue
        return ImageFont.load_default(size)

    font_handle = load_font(40)
    font_body = load_font(52)
    font_footer = load_font(36)

    # Draw Main Card
    card_x1, card_y1, card_x2, card_y2 = 100, 450, 980, 1350
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=45, fill=t["card"], outline=t["border"], width=6)

    # Avatar placeholder
    draw.rounded_rectangle([160, 510, 250, 600], radius=20, fill=t["bg"], outline=t["border"], width=3)
    draw.ellipse([185, 525, 225, 565], fill=t["text_mute"])
    draw.chord([170, 565, 240, 610], start=180, end=360, fill=t["text_mute"])

    # Fan Name
    display_name = f"@{fan_name.strip().replace('@', '')}" if fan_name.lower() != 'anonymous' else "Anonymous Fan"
    draw.text((280, 535), display_name, fill=t["text_mute"], font=font_handle)

    # Wrap text helper
    def wrap_text(text, max_chars=28):
        words = text.split()
        lines, current = [], ""
        for w in words:
            if len(f"{current} {w}".strip()) <= max_chars:
                current = f"{current} {w}".strip()
            else:
                lines.append(current)
                current = w
        if current: lines.append(current)
        return lines

    # Render Question
    y_offset = 640
    for line in wrap_text(question_text)[:4]:
        draw.text((160, y_offset), line, fill=t["text_main"], font=font_body)
        y_offset += 75

    # Draw separator line if there is an answer
    if answer_text:
        draw.line([160, y_offset + 10, 920, y_offset + 10], fill=t["border"], width=3)
        y_offset += 45
        draw.text((160, y_offset), "My Reply:", fill=t["accent"], font=font_handle)
        y_offset += 60
        for line in wrap_text(answer_text)[:4]:
            draw.text((160, y_offset), line, fill=t["text_main"], font=font_body)
            y_offset += 75

    draw.text((540, 1280), "SNAPCHAT DISCOVER FEEDS", fill=t["accent"], font=font_footer, anchor="ms")

    output_path = "snap_story_card.png"
    img.save(output_path)
    return output_path

# --- UI APP ROUTING ---
tab_fan, tab_creator = st.tabs(["📣 Ask Me Anything & Discover", "🔒 Creator Dashboard"])

# Force data initialization inside the secure session context
all_questions = load_questions()

# 1. FAN VIEW
with tab_fan:
    st.title("👻 Send Me a Question!")
    st.write("Fill out the form below to submit a question or dare for my next Snapchat Story!")

    with st.form("submission_form", clear_on_submit=True):
        fan_name = st.text_input("Your Name / Snapchat Handle", placeholder="Anonymous")
        question_text = st.text_area("Your Question", placeholder="What do you want to ask?", max_chars=280)
        submit_btn = st.form_submit_button("Send to Story Queue ✨")

        if submit_btn and question_text.strip():
            updated_qs = read_json_file() # Fresh disk read on submission
            updated_qs.append({
                "id": max((q["id"] for q in updated_qs), default=0) + 1,
                "fan_name": fan_name.strip() or "Anonymous",
                "question_text": question_text.strip(),
                "answer_text": "",
                "status": "pending",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            })
            save_questions(updated_qs)
            st.success("Sent! Look at the feed below or check my Snap stories to see if I pick yours! 🎉")
            st.rerun()

    # --- SNAPCHAT DISCOVER STYLE FEED ---
    st.markdown("---")
    st.header("✨ Snapchat Discover Feed")
    st.write("Browse through past featured questions and exclusive answers!")

    # Pull published questions cleanly from the thread context
    published_qs = [q for q in all_questions if q.get("status") == "published"][::-1]

    if not published_qs:
        st.info("Nothing featured on the Discover feed just yet. Check back soon!")

    for q in published_qs:
        st.markdown(
            f"""
            <div style="background-color: #111111; padding: 20px; border-radius: 15px; border-left: 5px solid #FFFC00; margin-bottom: 15px; color: white;">
                <span style="color: #888888; font-size: 0.85rem;">💬 Asked by <b>@{html.escape(q['fan_name'])}</b></span>
                <p style="font-size: 1.2rem; margin-top: 5px; margin-bottom: 10px; font-weight: bold;">"{html.escape(q['question_text'])}"</p>
                <div style="background-color: #222222; padding: 12px; border-radius: 10px; margin-top: 5px;">
                    <span style="color: #FFFC00; font-size: 0.85rem; font-weight: bold;">👻 Creator Reply:</span>
                    <p style="margin: 3px 0 0 0; color: #E0E0E0;">{html.escape(q.get('answer_text') or 'Viewed on Snapchat Story!')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 2. CREATOR DASHBOARD
with tab_creator:
    st.title("👑 Your Backstage Center")
    access_password = st.text_input("Enter Access Password", type="password")

    if access_password == PASSWORD:
        st.success("Access Granted.")

        st.subheader("🎨 Brand Customization")
        selected_theme = st.selectbox("Choose today's Story Aesthetic:", list(THEMES.keys()))

        # Sync queue state on load
        pending_qs = [q for q in all_questions if q["status"] == "pending"]

        st.subheader(f"📥 Pending Questions ({len(pending_qs)})")
        if not pending_qs:
            st.info("No questions in the queue yet.")

        for q in pending_qs:
            with st.container():
                st.markdown(f"**From:** @{q['fan_name']} *({q['timestamp']})*")
                st.write(f"\"{q['question_text']}\"")

                creator_reply = st.text_input("Write your short public reply (Optional):", key=f"ans_input_{q['id']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Generate Card 🎨", key=f"gen_{q['id']}"):
                        card_path = generate_snap_card(q['fan_name'], q['question_text'], selected_theme, creator_reply)
                        st.image(card_path, width=180)
                        with open(card_path, "rb") as file:
                            st.download_button("Download Image 📥", data=file, file_name=f"snap_card_{q['id']}.png", mime="image/png", key=f"dl_{q['id']}")

                with col2:
                    if st.button("Publish to Discover Feed 🚀", key=f"pub_{q['id']}"):
                        current_all_qs = read_json_file()
                        for item in current_all_qs:
                            if item["id"] == q["id"]:
                                item["status"] = "published"
                                item["answer_text"] = creator_reply if creator_reply else "Answered directly on stories!"
                        save_questions(current_all_qs)
                        st.success("Published! It is now live on your fan feed.")
                        st.rerun()
                st.markdown("---")
