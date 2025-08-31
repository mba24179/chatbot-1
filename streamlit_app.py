import streamlit as st
from openai import OpenAI

# Initialize API key
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["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"]
    client = OpenAI(api_key=OPENAI_API_KEY)
    demo_mode = False
else:
    client = None
    demo_mode = True

st.title("🤖 ChaufX Concierge")
st.write("Your premium chauffeur booking assistant.")

# Chat input
user_input = st.text_input("You:", "")

if user_input:
    if demo_mode:
        st.warning("⚠️ No API key found. Running in demo mode.")
        st.success("✅ (Demo Mode) Booking confirmed! Pickup: Connaught Place → Drop: Delhi Airport → Tomorrow 8 AM")
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ChaufX Concierge, a premium chauffeur booking assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        st.write("ChaufX Concierge:", response.choices[0].message.content)
