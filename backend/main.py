from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from loguru import logger

from .index_manager import load_or_build, rebuild
from .rag_engine import build_query_engine
from .file_manager import save_upload

import os
from .config import DATA_DIR


app = FastAPI(title="Local AI Document Chat")

@app.get("/files")
def list_files():
    return {"files": os.listdir(DATA_DIR)}

# ---------- CORS (allow local frontend) ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load index at startup ----------

logger.info("Loading index...")
index = load_or_build()
engine = build_query_engine(index)
logger.info("Ready.")

# ---------- Background rebuild ----------

def rebuild_bg():
    global index, engine
    logger.info("Rebuilding index...")
    index = rebuild()
    engine = build_query_engine(index)
    logger.info("Index rebuilt.")


# ---------- Upload Endpoint ----------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    bg: BackgroundTasks = None
):
    try:
        save_upload(file)
        bg.add_task(rebuild_bg)

        return {
            "status": "uploaded",
            "filename": file.filename,
            "indexing": "started"
        }

    except Exception as e:
        logger.exception("Upload failed")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ---------- Chat Endpoint (Streaming + Memory) ----------

from fastapi.responses import StreamingResponse, JSONResponse
from llama_index.llms.ollama import Ollama

# ---------- small talk router ----------

SMALL_TALK = {
    "hi", "hello", "hey", "yo",
    "thanks", "thank you",
    "good morning", "good evening"
}

def is_smalltalk(q: str):
    q = q.lower().strip()
    if q in SMALL_TALK:
        return True
    if len(q.split()) <= 2 and q not in ("phase", "explain", "define"):
        return True
    return False


# ---------- upgraded chat endpoint ----------

@app.post("/chat")
async def chat(data: dict):

    try:
        user_q = data.get("message", "").strip()
        memory = data.get("memory", [])

        if not user_q:
            return JSONResponse(
                status_code=400,
                content={"error": "empty message"}
            )

        # ---------- small talk path ----------

        if is_smalltalk(user_q):

            llm = Ollama(model="llama3.1", temperature=0.6)

            def smalltalk_stream():
                try:
                    resp = llm.complete(user_q)
                    yield resp.text
                except Exception:
                    yield "Hello 🙂"

            return StreamingResponse(
                smalltalk_stream(),
                media_type="text/plain"
            )

        # ---------- build memory context ----------

        mem_text = "\n".join(
            f'{m["role"]}: {m["text"]}'
            for m in memory[-4:]
        )

        final_query = (
            user_q if not mem_text
            else mem_text + "\nUser: " + user_q
        )

        logger.info(f"Query → {user_q}")

        # ---------- RAG stream ----------

        def stream():
            try:
                resp = engine.query(final_query)
                text = str(resp).strip()

                if not text or len(text) < 5:
                    yield "Not in uploaded sources."
                    return

                yield text

            except Exception:
                logger.exception("RAG QUERY FAIL")
                yield "Not in uploaded sources."



        return StreamingResponse(
            stream(),
            media_type="text/plain"
        )

    except Exception as e:
        logger.exception("CHAT FAIL")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )



# ---------- Health Check ----------

@app.get("/health")
def health():
    return {"status": "ok"}

SMALL_TALK = {
    "hi","hello","hey","thanks","thank you","yo"
}

def is_smalltalk(q):
    q = q.lower().strip()
    return q in SMALL_TALK or len(q.split()) <= 2
