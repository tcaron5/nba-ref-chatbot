from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    """Entry point: rebuild the Chroma database from local documents."""
    generate_data_store()


def generate_data_store():
    """Load raw documents, split them into chunks, and save embeddings to Chroma."""
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    """Load all Markdown files from the data/ directory into LangChain Document objects."""
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    """
    Split documents into smaller overlapping chunks for better retrieval.
    
    - chunk_size=300: max characters per chunk
    - chunk_overlap=60: overlap to preserve context across boundaries
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=60,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Example: print out one chunk for inspection/debugging
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    """
    Save text chunks into a persistent Chroma vector database.

    - Clears existing DB (if any)
    - Embeds each chunk using MiniLM
    - Persists the new database to disk
    """
    # Clear out the existing database directory
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create and persist a new DB
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()