# NBA Ref Chatbot

> An AI-powered chatbot to help you distinguish between legal and illegal plays in the NBA, answer rules questions, and provide instant reference to official NBA rules.

---

## Features

- **Natural Language Chat**: Ask questions about NBA rules, fouls, penalties, and more.
- **Retrieval-Augmented Generation (RAG)**: Combines a local LLM (Zephyr-7B) with a vector database of official NBA rules for accurate, context-aware answers.
- **Modern React Frontend**: Clean, responsive chat UI for easy interaction.
- **Fast, Local Inference**: All data and models run locally—no cloud or API keys required.

## Quickstart

### 1. Requirements

- Python 3.10+
- Node.js 18+
- ~5GB RAM (for LLM)

### 2. Setup

#### Backend

```bash
pip install -r requirements.txt
# Place Zephyr-7B GGUF model in project root (see below)
python database.py    # (first run: builds vector DB)
python backend.py     # (starts Flask API)
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Model File

Download zephyr-7b-beta.Q5_K_M.gguf from HuggingFace or your preferred source.
Place it in the project root (not included in repo).

### 4. Usage

Open the frontend in your browser (default: http://localhost:5173)
Ask any question about the NBA rules in the chat!

## File Structure

- database.py, query.py, backend.py: Backend logic and API
- data/: Official NBA rules in markdown
- frontend/: React app (UI)
- zephyr-7b-beta.Q5_K_M.gguf: LLM weights (not included)
- chroma/: Vector DB (auto-generated)

## Notes

- Model and DB files are gitignored. Download the model separately.
