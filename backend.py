

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import CTransformers

local_llm = "zephyr-7b-beta.Q5_K_M.gguf"
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are Scott Foster, an esteemed NBA referee with years of experience. Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

app = Flask(__name__)
CORS(app)

# Load database and model once at startup
print("Loading vector database...")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
print("Vector database loaded.")

print("Loading LLM...")
config = {
    'max_new_tokens': 1024,
    'repetition_penalty': 1.1,
    'temperature': 0.1,
    'top_k': 50,
    'top_p': 0.9,
    'stream': True,
    'threads': os.cpu_count(),
}
llm = CTransformers(
    model=local_llm,
    model_type="Zephyr-7B-beta",
    **config
)
print("LLM loaded.")

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint.
    - Accepts JSON { "message": "..." }
    - Retrieves relevant context from the vector DB
    - Formats a prompt with that context + user question
    - Generates a response with the local LLM
    - Returns JSON { "reply": "..." }
    """
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'reply': 'No message provided.'}), 400

    # Step 1: Search vector database for top-k relevant chunks
    results = db.similarity_search_with_relevance_scores(user_message, k=3)
    if not results:
        return jsonify({'reply': 'No relevant context found.'})

    # Extract and join chunk texts
    chunk_texts = [doc.page_content for doc, _score in results]
    context_text = "\n\n---\n\n".join(chunk_texts)

    # Step 2: Build prompt with retrieved context
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_message)

    # Step 3: Generate response from the LLM
    response_text = llm.invoke(prompt)

    # Collect sources (filenames, if present)
    sources = [doc.metadata.get("source", None) for doc, _score in results]

    # Step 4: Construct formatted response (includes chunks + sources for transparency)
    chunks_section = "\n\n".join(chunk_texts)
    formatted_response = (
        f"Chunks referenced:\n{chunks_section}\n\n"
        f"{response_text}\n\n"
        f"Sources: {sources}"
    )
    return jsonify({'reply': formatted_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
