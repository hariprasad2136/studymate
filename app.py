# app.py
import streamlit as st
from utils import load_model, ask_question
from model import extract_text_from_pdf

# Session state to persist model and context
if "model_client" not in st.session_state:
    st.session_state.model_client = None
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

st.set_page_config(page_title="📄 PDF Q&A with IBM Granite", layout="wide")

st.title("📄 PDF Question Answering with IBM Granite")

# --- Step 1: Authenticate ---
st.subheader("🔑 Enter your Hugging Face Token")
token = st.text_input("Hugging Face Token", type="password")
if st.button("Load Model"):
    try:
        st.session_state.model_client = load_model(token)
        st.success("✅ Granite model loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to load Granite model: {e}")

# --- Step 2: Upload PDF ---
st.subheader("📂 Upload PDF File")
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf is not None:
    try:
        st.session_state.pdf_context = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Extracted Text Preview", st.session_state.pdf_context[:2000], height=300)
    except Exception as e:
        st.error(f"Error processing PDF: {e}")

# --- Step 3: Ask Question ---
st.subheader("❓ Ask a Question")
question = st.text_input("Type your question here:")

if st.button("Get Answer"):
    if st.session_state.model_client is None:
        st.warning("⚠ Please load the model with your Hugging Face token first.")
    elif not st.session_state.pdf_context:
        st.warning("⚠ Please upload and process a PDF first.")
    else:
        answer = ask_question(st.session_state.model_client, st.session_state.pdf_context, question)
        st.text_area("💡 Answer", answer, height=200)
