# Vox AI — Enterprise Meeting Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-Deployed-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge" />
</p>

---

# 🚀 Overview

Vox AI is an advanced AI-powered Meeting Intelligence Platform designed to transform raw conversations into actionable insights.

The platform enables users to upload audio files or YouTube links, transcribe conversations, generate intelligent summaries, extract key decisions, and interact with meeting content using a Retrieval-Augmented Generation (RAG) conversational system.

Built with modern AI infrastructure including LangChain, ChromaDB, Whisper, HuggingFace Embeddings, and Mistral AI.

---

# ✨ Core Features

## 🎙 Intelligent Transcription
- Supports YouTube URLs and local audio/video files
- AI-powered speech recognition using OpenAI Whisper
- Handles multilingual and Hinglish conversations

## 🧠 AI Meeting Summarization
- Generates concise meeting summaries
- Extracts:
  - Key discussion points
  - Action items
  - Decisions taken
  - Open questions

## 💬 RAG-Powered AI Chat
- Chat with uploaded meeting content
- Context-aware responses
- Semantic retrieval using vector embeddings

## 🔍 Semantic Search Engine
- ChromaDB vector storage
- HuggingFace sentence-transformer embeddings
- Fast contextual retrieval pipeline

## 🌐 Multilingual Support
- English
- Hindi
- Hinglish
- Translation support included

## ⚡ Modern UI
- Responsive Streamlit interface
- Professional dashboard experience
- Real-time processing workflow

---

# 🏗 System Architecture

```text
User Input
   │
   ▼
Whisper Transcription
   │
   ▼
Text Processing & Chunking
   │
   ▼
Embedding Generation
   │
   ▼
ChromaDB Vector Store
   │
   ▼
LangChain Retrieval Pipeline
   │
   ▼
Mistral AI Response Engine
```

---

# 🛠 Tech Stack

| Category | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| AI Framework | LangChain |
| LLM | Mistral AI |
| Speech Recognition | OpenAI Whisper |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace |
| Translation | Deep Translator |
| Audio Processing | FFmpeg / Pydub |

---

# 📂 Project Structure

```bash
meeting-summarizer-ai/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── downloads/
├── vector_db/
├── utils/
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Swain-Sanjay/meeting-summarizer-ai.git
```

## Move Into Project

```bash
cd meeting-summarizer-ai
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run Application

```bash
streamlit run app.py
```

---

# 🌍 Live Demo

## Streamlit Deployment

https://meeting-summarizer-ai-3dtciqj5mwdqvmgbnuimju.streamlit.app

---

# 📸 Capabilities

- ✔ AI transcription
- ✔ Meeting summarization
- ✔ Contextual retrieval
- ✔ Semantic search
- ✔ Conversational AI
- ✔ Multilingual support
- ✔ YouTube processing
- ✔ Local file upload

---

# 🔐 Future Improvements

- User authentication
- Cloud database integration
- Real-time collaboration
- Speaker diarization
- Export to PDF / DOCX
- Team workspace support
- API integration
- Analytics dashboard

---

# 👨‍💻 Author

## Sanjay Kumar Swain

AI Developer • Python Developer • Agentic AI Enthusiast

GitHub:
https://github.com/Swain-Sanjay

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful:

- Star the repository
- Share the project
- Contribute improvements

---

# 💡 Vision

Vox AI aims to simplify human conversations using AI-powered intelligence systems that convert meetings into searchable, actionable knowledge.
