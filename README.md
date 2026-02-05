# Local AI

This AI Bot can analyze the documents uploaded by you and answer any question that you may ask to it.  
(It only answers questions referring to the knowledge provided in the uploaded documents.)

The system runs locally using a local LLM through Ollama and a Retrieval-Augmented Generation (RAG) pipeline. After initial model downloads, it works fully offline.

------------------------------------------------------------------------------------------------------------

# What This Bot Can Do

- Analyze uploaded documents (PDF, DOCX, TXT, Markdown, etc.)
- Answer questions strictly from uploaded sources
- Refuse answers if information is not found in documents
- Perform semantic search over document content
- Use reranking to improve answer relevance
- Show uploaded files in sidebar
- Save uploaded files locally on your device
- Persist chat history across page reloads
- Work offline after first model setup

------------------------------------------------------------------------------------------------------------

# Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- FastAPI
- LlamaIndex (RAG framework)

AI Layer:
- Ollama (local LLM runtime)
- HuggingFace embeddings
- SentenceTransformers reranker

------------------------------------------------------------------------------------------------------------

# Project Structure
```
├── backend/
│ ├── main.py
│ ├── config.py
│ ├── rag_engine.py
│ ├── index_manager.py
│ ├── file_manager.py
│ └── init.py
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── app.js
│
├── data/ # uploaded documents saved here
├── storage/ # vector index stored here
├── logs/
└── venv/
```


------------------------------------------------------------------------------------------------------------

# Requirements

- Python 3.10 or higher
- Ollama installed
- 16 GB RAM recommended
- macOS / Linux / Windows supported

------------------------------------------------------------------------------------------------------------
 # Python Dependencies (Required)

pip install fastapi uvicorn
pip install llama-index
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface
pip install sentence-transformers
pip install chromadb
pip install python-multipart
pip install pypdf python-docx
pip install loguru

------------------------------------------------------------------------------------------------------------

#To Run

1. Clone repo to your local machine.
    "in bash"
     git clone <your-repo-url>
     cd local-ai-chat

2. Create a virtual environment.
   "in bash"
   python3 -m venv venv
   source venv/bin/activate
   
   "windows"
   venv\Scripts\activate

3. Install dependencies.
   pip install -r requirements.txt

4. Start Ollama server (leave it runnning).
  "in bash"
  ollama serve

5. Start backend server (In new terminal window).
   source venv/bin/activate
   uvicorn backend.main:app --reload

6. Open frontend in your browser.
   frontend/index.html

7. Upload documents from the left sidebar and start chatting.
   
------------------------------------------------------------------------------------------------------------

# How It Works

1. Uploaded files are saved locally in the data/ folder
2. Documents are chunked and embedded
3. Vector index is stored in storage/
4. Queries use semantic retrieval + reranking
5. Only grounded answers are returned
6. Chat history is saved in browser local storage
   
------------------------------------------------------------------------------------------------------------

# Troubleshooting

1. Ollama connection error
    Start Ollama: "ollama serve"

2. Model not found
    "ollama pull llama3.1"

3. Backend not reachable
    Check backend is running: "uvicorn backend.main:app --reload"

Test:
http://127.0.0.1:8000/health

Rebuild index
rm -rf storage/*

Restart backend : (control + c) then "uvicorn backend.main:app --reload" .

------------------------------------------------------------------------------------------------------------
# License

MIT License

