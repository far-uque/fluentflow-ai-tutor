import streamlit as st
import requests

st.set_page_config(page_title="FluentFlow AI Tutor", page_icon="🧠")

st.title("🧠 FluentFlow: English Tutor for Bengali Speakers")

st.markdown("""
FluentFlow is your AI-powered assistant for learning English.  
✅ Translate English to Bengali  
✅ Explain difficult words and phrases  
✅ Simple, free, and open-source
""")

# Hugging Face API key input (optional)
hf_token = st.text_input("🔐 Enter your Hugging Face API Token", type="password")

# Input area
english_input = st.text_area("✍️ Enter English text to translate and explain")

col1, col2 = st.columns(2)

def translate_to_bengali(text, hf_token):
    API_URL = "https://api-inference.huggingface.co/models/ai4bharat/indictrans2-en-bn"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result[0].get("translation_text", "⚠️ Could not translate")
    except Exception as e:
        return f"❌ Error: {e}"

def explain_text(text, hf_token):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {hf_token}"}
    prompt = f"Explain this English sentence in simpler words: {text}"
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "⚠️ Could not explain")
    except Exception as e:
        return f"❌ Error: {e}"

# Translate Button
if col1.button("🌐 Translate to Bengali"):
    if not english_input or not hf_token:
        st.warning("Please enter text and a Hugging Face token.")
    else:
        with st.spinner("Translating..."):
            translation = translate_to_bengali(english_input, hf_token)
        st.success("✅ Bengali Translation")
        st.write(translation)

# Explain Button
if col2.button("🧠 Explain in Easy English"):
    if not english_input or not hf_token:
        st.warning("Please enter text and a Hugging Face token.")
    else:
        with st.spinner("Explaining..."):
            explanation = explain_text(english_input, hf_token)
        st.success("✅ Explanation")
        st.write(explanation)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Hugging Face, and open-source tools.")
