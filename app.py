import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE

import os

MODEL_NAME = "gemini-3.8-flash"
st.set_page_config(page_title="ReceiptSnap", page_icon="🧾")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS") or st.secrets.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") or st.secrets.get("GMAIL_APP_PASSWORD", "")

if not GEMINI_API_KEY or not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
    st.error(
        "Missing required secrets. Add GEMINI_API_KEY, GMAIL_ADDRESS, and GMAIL_APP_PASSWORD in Streamlit Cloud > Settings > Secrets or set them as environment variables."
    )
    st.stop()


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])


def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"


def send_email(to_address, subject, body):
    try:
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = GMAIL_ADDRESS
        message["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(message)
        return True, "Email sent successfully!"
    except Exception as error:
        return False, str(error)


# Step 1: Onboarding
if "onboarded" not in st.session_state:
    st.title("🧾 ReceiptSnap & Bill Splitter")
    st.caption("Snap receipts. Calculate splits. Email summary to yourself.")
    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        user_email = st.text_input("Your Email address", placeholder="name@example.com")
        submitted = st.form_submit_button("Start Splitting 🚀")
    if submitted:
        if not name.strip() or not user_email.strip():
            st.warning("Please fill in both your name and email address.")
        else:
            st.session_state.name = name.strip()
            st.session_state.user_email = user_email.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

# Step 2: Chat UI
header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("🧾 ReceiptSnap")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button("📧 Send via Email", disabled=send_disabled, use_container_width=True):
        with st.spinner("Preparing summary..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_email(
            st.session_state.user_email,
            f"ReceiptSnap Expense Summary for {st.session_state.name}",
            summary,
        )
        if success:
            st.success("Sent! Check your inbox 📬")
        else:
            st.error(f"Couldn't send email: {info}")

st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.user_email}")

if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Ask a question or upload a receipt photo...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("Analyze this receipt and give me an itemized total and breakdown.")

    with st.spinner("Processing receipt..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)
