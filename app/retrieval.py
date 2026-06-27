from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# Embedding Model (Loaded Once)
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)


# --------------------------------------------------
# Chunking
# --------------------------------------------------

def create_chunks(transcript: str):
    """
    Split transcript into semantic chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    return splitter.create_documents([transcript])


# --------------------------------------------------
# Vector Store
# --------------------------------------------------

def create_vector_store(chunks):
    """
    Create FAISS vector database.
    """

    return FAISS.from_documents(
        chunks,
        embeddings,
    )


# --------------------------------------------------
# Retriever
# --------------------------------------------------

def create_retriever(vector_store):
    """
    Create retriever.
    """

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "lambda_mult": 0.7,
        },
    )