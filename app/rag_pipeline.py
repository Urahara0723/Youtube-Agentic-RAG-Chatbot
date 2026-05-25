from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.prompts import SUMMARY_PROMPT
from app.config import OPENROUTER_API_KEY


def create_chunks(transcript: str) -> list:
    """
    Split transcript into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = splitter.create_documents([transcript])

    return chunks


def create_vector_store(chunks) -> FAISS:
    """
    Create FAISS vector store using embeddings.
    """

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store


def create_retriever(vector_store):
    """
    Create retriever from vector store.
    """

    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )

    return retriever


def generate_answer(retriever, question: str):
    """
    Generate final answer using retrieved context + LLM.
    """

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = PromptTemplate(
        template=SUMMARY_PROMPT, input_variables=["context", "question"]
    )

    final_prompt = prompt.format(context=context, question=question)

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        model="openai/gpt-oss-120b:free",
        temperature=0.2,
    )

    response = llm.invoke(final_prompt)

    return response.content
