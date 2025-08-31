import streamlit as st
from openai import OpenAI

# Get the API key safely
OPENAI_API_KEY = st.secrets["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"]
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("🤖 ChaufX Concierge")
st.write("Your premium chauffeur booking assistant.")

user_input = st.text_input("You:", "")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are ChaufX Concierge, a premium chauffeur booking assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    st.write("ChaufX Concierge:", response.choices[0].message.content)
