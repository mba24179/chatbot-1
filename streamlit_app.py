# streamlit_app.py
import streamlit as st
from openai import OpenAI, RateLimitError, AuthenticationError
import re

# === Page Setup ===
st.set_page_config(
    page_title="ChaufX Concierge",
    page_icon="🚘",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("🤖 ChaufX Concierge")
st.markdown("Your premium chauffeur booking assistant.")

# === Load OpenAI Client ===
if "OPENAI_API_KEY" in st.secrets:
    try:
        client = OpenAI(api_key=st.secrets["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"])
        key_available = True
    except Exception:
        client = None
        key_available = False
else:
    client = None
    key_available = False

# === Helper Functions ===
def safe_chat(user_input: str) -> str:
    """Calls OpenAI API, with fallback for rate-limit or missing key."""
    if not key_available or client is None:
        return demo_booking_response()
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are ChaufX Concierge, a premium chauffeur booking assistant.
1. Confirm booking with ✅ when pickup, drop, date, time are provided.
2. Answer FAQs concisely and professionally.
"""
                },
                {"role": "user", "content": user_input}
            ]
        )
        return resp.choices[0].message.content
    except RateLimitError:
        return demo_booking_response()
    except AuthenticationError:
        return "⚠️ Invalid API key. Please check your Streamlit Secrets."
    except Exception as e:
        return f"⚠️ Error occurred: {str(e)}"

def demo_booking_response() -> str:
    return ("✅ (Demo Mode) Booking confirmed!\n"
            "Pickup: Connaught Place\n"
            "Drop: Delhi Airport\n"
            "Date: Tomorrow\n"
            "Time: 8 AM\n"
            "Driver: Rajesh Kumar 🚖\n"
            "Car: Mercedes S-Class")

def format_chat_history():
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# === Chat UI ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_reply = safe_chat(user_input)
    st.session_state.chat_history.append(("ChaufX Concierge", bot_reply))

format_chat_history()
