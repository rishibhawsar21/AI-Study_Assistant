import PyPDF2
from transformers import pipeline
from openai import OpenAI
import streamlit as st
import os
from io import BytesIO
import requests
from datasets import load_dataset


# CONFIGURATION SECTION - ADD YOUR KEYS HERE
# OpenAI API Key
OPENAI_API_KEY = "Enter your OpenAI API key here"  # Get from: https://platform.openai.com/api-keys

# Hugging Face Token (optional, for private models or higher rate limits)
HUGGING_FACE_TOKEN = "Enter your Hugging Face token here (Its optional)"  # Get from: https://huggingface.co/settings/tokens

# PDF URLs for testing
PDF_URLS = {
    "Sample 1": r"C:\Users\DELL\OneDrive\Desktop\LLM Embeddings Explained .pdf"
}

# HELPER FUNCTIONS

def download_pdf_from_url(url):
    """Download PDF from URL and return as BytesIO object"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"Error downloading PDF: {str(e)}")
        return None


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file (works with file path or BytesIO object)"""
    text = ""
    try:
        # Handle different input types
        if isinstance(pdf_file, str):
            # File path
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        else:
            # BytesIO or file-like object (from Streamlit upload or URL)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return ""
    
    return text


def summarize_text(text, max_length=150, min_length=30):
    """Summarize text using Hugging Face transformer"""
    try:
        # Initialize with token if provided
        if HUGGING_FACE_TOKEN and HUGGING_FACE_TOKEN != "your-huggingface-token-here":
            summarizer = pipeline("summarization", token=HUGGING_FACE_TOKEN)
        else:
            summarizer = pipeline("summarization")
        
        # Split long text into chunks (transformers have token limits)
        max_chunk = 1024
        if len(text) > max_chunk:
            text = text[:max_chunk]
        
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error summarizing: {str(e)}"


def ask_question(question, context):
    """Answer questions about the document using Hugging Face model"""
    try:
        if HUGGING_FACE_TOKEN and HUGGING_FACE_TOKEN != "your-huggingface-token-here":
            qa_model = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad",
                token=HUGGING_FACE_TOKEN
            )
        else:
            qa_model = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad"
            )
        
        # Limit context length
        max_context = 512
        if len(context) > max_context:
            context = context[:max_context]
        
        answer = qa_model(question=question, context=context)
        return answer['answer']
    except Exception as e:
        return f"Error answering question: {str(e)}"


def ask_gpt(prompt):
    """Use OpenAI GPT for advanced features"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with GPT: {str(e)}"


# STREAMLIT WEB INTERFACE

def main():
    st.title("🎓 AI Study Assistant")
    st.write("Upload a PDF or load from URL to get summaries and ask questions!")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check API keys
        if OPENAI_API_KEY == "your-openai-api-key-here":
            st.warning("⚠️ OpenAI API key not set")
        else:
            st.success("✅ OpenAI API configured")
        
        if HUGGING_FACE_TOKEN == "your-huggingface-token-here":
            st.info("ℹ️ Hugging Face token not set (optional)")
        else:
            st.success("✅ Hugging Face token configured")
        
        st.markdown("---")
        st.markdown("**How to get API keys:**")
        st.markdown("- [OpenAI API](https://platform.openai.com/api-keys)")
        st.markdown("- [Hugging Face](https://huggingface.co/settings/tokens)")
    
    # Choose input method
    input_method = st.radio("Choose input method:", ["Upload PDF", "Load from URL", "Use Local File"])
    
    text = None
    
    if input_method == "Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file:
            with st.spinner("Extracting text..."):
                text = extract_text_from_pdf(uploaded_file)
    
    elif input_method == "Load from URL":
        # Option 1: Select from predefined URLs
        if PDF_URLS:
            selected_pdf = st.selectbox("Select a PDF:", list(PDF_URLS.keys()))
            if st.button("Load Selected PDF"):
                with st.spinner("Downloading PDF..."):
                    pdf_file = download_pdf_from_url(PDF_URLS[selected_pdf])
                    if pdf_file:
                        text = extract_text_from_pdf(pdf_file)
        
        # Option 2: Enter custom URL
        st.write("Or enter a custom URL:")
        custom_url = st.text_input("PDF URL:")
        if custom_url and st.button("Load Custom PDF"):
            with st.spinner("Downloading PDF..."):
                pdf_file = download_pdf_from_url(custom_url)
                if pdf_file:
                    text = extract_text_from_pdf(pdf_file)
    
    else:  # Use Local File
        local_path = st.text_input("Enter local PDF path:", "sample.pdf")
        if st.button("Load Local File"):
            if os.path.exists(local_path):
                with st.spinner("Extracting text..."):
                    text = extract_text_from_pdf(local_path)
            else:
                st.error(f"File not found: {local_path}")
    
    # Display extracted text
    if text:
        with st.expander("📄 View Extracted Text"):
            st.text_area("Extracted Text", text, height=200)
        
        st.success(f"✅ Extracted {len(text)} characters")
        
        # Choose task
        task = st.radio("Choose a task:", ["Summarize", "Ask a Question", "GPT Analysis"])
        
        if task == "Summarize":
            if st.button("Generate Summary"):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(text)
                    st.write("**Summary:**")
                    st.info(summary)
        
        elif task == "Ask a Question":
            question = st.text_input("Enter your question:")
            if question and st.button("Get Answer"):
                with st.spinner("Finding answer..."):
                    answer = ask_question(question, text)
                    st.write("**Answer:**")
                    st.success(answer)
        
        else:  # GPT Analysis
            st.write("Use GPT-4 for advanced analysis")
            prompt_type = st.selectbox(
                "Choose analysis type:",
                ["Summarize", "Key Points", "Custom Prompt"]
            )
            
            if prompt_type == "Custom Prompt":
                custom_prompt = st.text_area("Enter your prompt:")
                prompt = custom_prompt + "\n\nDocument:\n" + text[:2000]
            elif prompt_type == "Key Points":
                prompt = "List the key points from this document:\n\n" + text[:2000]
            else:
                prompt = "Summarize this document concisely:\n\n" + text[:2000]
            
            if st.button("Analyze with GPT"):
                with st.spinner("Analyzing with GPT-4..."):
                    result = ask_gpt(prompt)
                    st.write("**GPT-4 Analysis:**")
                    st.markdown(result)


if __name__ == "__main__":
    main()