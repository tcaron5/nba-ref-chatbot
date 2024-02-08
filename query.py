import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import ChatPromptTemplate
import os
from langchain.llms import CTransformers
#from langchain.chains import RetrievalQA
import gradio as gr

local_llm = "zephyr-7b-beta.Q5_K_M.gguf"
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Creating CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Preparing database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))

    # Searching database
    results = db.similarity_search_with_relevance_scores(query_text, k=2)
    #if len(results) == 0 or results[0][1] < 0.7:
    #    print(f"Unable to find matching results.")
    #    return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    
    config = {
    'max_new_tokens': 1024, 
    'repetition_penalty': 1.1,
    'temperature': 0.1,
    'top_k': 50,
    'top_p': 0.9,
    'stream': True,
    'threads': os.cpu_count() #int(os.cpu_count() / 2)
    }

    llm_init = CTransformers(
    model=local_llm,
    model_type="Zephyr-7B-beta",
    **config)

    print("LLM Initialized...")


    response_text = llm_init.invoke(prompt)
    print("Response received...")

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)



if __name__ == "__main__":
    main()