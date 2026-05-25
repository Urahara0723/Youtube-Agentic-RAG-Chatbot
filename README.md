# YouTube RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that answers questions about YouTube videos using transcript-based semantic search.

This project extracts transcripts from YouTube videos, converts them into embeddings, stores them in a FAISS vector database, retrieves relevant context, and generates responses using an open source LLM through OpenRouter.

---

## Features

- YouTube transcript extraction
- Semantic search using FAISS vector database
- Retrieval-Augmented Generation (RAG)
- Question answering over video transcripts
- OpenRouter LLM integration
- Modular Python project structure
- Streamlit-based interface

---

## Tech Stack

- Python
- LangChain
- FAISS
- HuggingFace Embeddings
- OpenRouter
- Streamlit
- YouTube Transcript API

---

## Project Structure

```bash
youtube-rag-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── prompts.py
│   ├── rag_pipeline.py
│   ├── transcript.py
│   └── utils.py
│
├── streamlit_app.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/youtube-rag-chatbot.git

cd youtube-rag-chatbot
```

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory.

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## Running the Project

### Terminal Version

```bash
python -m app.main
```

---

### Streamlit Version

```bash
streamlit run streamlit_app.py
```

---

## System Architecture

```text
YouTube Video
      ↓
Transcript Extraction
      ↓
Text Chunking
      ↓
Embeddings Generation
      ↓
FAISS Vector Store
      ↓
Semantic Retrieval
      ↓
LLM (OpenRouter)
      ↓
Final AI Response
```

---

## Example Questions

- What is MCP?
- Summarize the video
- What did the speaker say about Tiny LLMs?
- What are the key takeaways from the video?

---

## Future Improvements

- Timestamp-based retrieval
- Chat history
- Multi-video support
- Improved UI/UX
- Retrieval caching
- Source citations

---

## Author

Mohit Trivedi, student at IIT Roorkee.