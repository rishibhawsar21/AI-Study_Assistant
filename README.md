# 🎓 AI Study Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent PDF analysis tool powered by AI that helps students and professionals extract insights, generate summaries, and get instant answers from their documents.

![AI Study Assistant Demo](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=AI+Study+Assistant+Demo)

## ✨ Features

- 📄 **PDF Text Extraction** - Upload PDFs or load from URLs/local files
- 🤖 **AI-Powered Summarization** - Get concise summaries using Hugging Face transformers
- 💬 **Question Answering** - Ask questions and get context-aware answers
- 🧠 **GPT-4 Integration** - Advanced analysis with OpenAI's GPT-4
- 🎯 **Multiple Input Methods** - Upload, URL, or local file support
- 🚀 **Easy to Use** - Clean Streamlit interface

## 🎬 Demo

**Try it yourself:**
1. Upload a PDF document
2. Get instant summaries
3. Ask questions about the content
4. Use GPT-4 for deep analysis

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Hugging Face Transformers (DistilBERT)
  - OpenAI GPT-4
- **PDF Processing**: PyPDF2
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Hugging Face token (optional, [Get one here](https://huggingface.co/settings/tokens))

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
HUGGING_FACE_TOKEN=your_huggingface_token_here
```

Or edit the `config.py` file directly (see Configuration section).

### 5. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## ⚙️ Configuration

### Option 1: Environment Variables (Recommended)

Create a `.env` file:
```env
OPENAI_API_KEY=sk-...
HUGGING_FACE_TOKEN=hf_...
```

### Option 2: Direct Configuration

Edit the `config.py` file:
```python
OPENAI_API_KEY = "your-api-key"
HUGGING_FACE_TOKEN = "your-token"
```

⚠️ **Security Note**: Never commit your API keys to GitHub. Always use environment variables or `.env` files (which should be in `.gitignore`).

## 📖 Usage

### 1. Upload a PDF
- Click "Browse files" to upload a PDF
- Or enter a URL to load a remote PDF
- Or specify a local file path

### 2. View Extracted Text
- Expand the "View Extracted Text" section
- Review the extracted content

### 3. Choose Your Task

#### Summarize
- Click "Generate Summary" for a concise overview
- Powered by Hugging Face transformers

#### Ask Questions
- Type your question in the input box
- Get instant, context-aware answers
- Uses DistilBERT for accurate responses

#### GPT-4 Analysis
- Choose from preset prompts or write custom ones
- Get advanced insights using OpenAI's GPT-4
- Perfect for deep document analysis

## 📁 Project Structure

```
ai-study-assistant/
│
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
├── README.md            # This file
│
├── utils/
│   ├── pdf_processor.py # PDF extraction utilities
│   ├── ai_models.py     # AI model interfaces
│   └── helpers.py       # Helper functions
│
└── tests/
    └── test_app.py      # Unit tests
```

## 🔧 Dependencies

```
streamlit>=1.28.0
PyPDF2>=3.0.0
transformers>=4.30.0
openai>=1.0.0
requests>=2.31.0
python-dotenv>=1.0.0
torch>=2.0.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large PDFs (>50 pages) may take longer to process
- Some PDF formats with complex layouts may not extract perfectly
- Transformer models have token limits (~1024 tokens)

## 🗺️ Roadmap

- [ ] Add support for more file formats (DOCX, TXT)
- [ ] Implement chat history for follow-up questions
- [ ] Add export functionality for summaries
- [ ] Support for multiple language documents
- [ ] Implement caching for faster repeated queries
- [ ] Add batch processing for multiple documents


## 👨‍💻 Author

**Your Name**
- GitHub: [@rishibhawsar21](https://github.com/rishibhawsar21)
- LinkedIn: www.linkedin.com/in/rishikesh-bhawsar-b884b8229

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4 API
- [Hugging Face](https://huggingface.co/) for transformer models
- [Streamlit](https://streamlit.io/) for the amazing framework
- All contributors who help improve this project

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-study-assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-study-assistant?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/ai-study-assistant)

---

⭐ If you find this project useful, please consider giving it a star!

