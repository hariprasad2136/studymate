# utils.py
from huggingface_hub import InferenceClient

# Use a valid Granite model ID
MODEL_ID = "ibm-granite/granite-3.2-8b-instruct"   # you can switch to 3.1-2b-instruct if you want smaller

def load_model(token: str):
    """
    Load Granite model client using Hugging Face Inference API.
    """
    try:
        client = InferenceClient(
            model=MODEL_ID,
            token=token
        )
        return client
    except Exception as e:
        raise RuntimeError(f"Error loading model {MODEL_ID}: {str(e)}")

def ask_question(client, context: str, question: str) -> str:
    """
    Send context + question to the Granite model and return answer.
    """
    try:
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        response = client.text_generation(
            prompt,
            max_new_tokens=300,
            temperature=0.2
        )
        return response
    except Exception as e:
        # Return full error message to Streamlit
        return f"❌ Error generating answer: {str(e)}"
