import streamlit as st

from langchain_core.messages import HumanMessage

from app.chatbot import chatbot, set_retriever


from app.transcript import (
    extract_video_id,
    get_transcript,
)

from app.rag_pipeline import (
    create_chunks,
    create_vector_store,
    create_retriever,
)

st.set_page_config(
    page_title="YouTube Agentic RAG Chatbot",
    page_icon="🎥",
    layout="wide",
)

st.title("🎥 YouTube AI Assistant")

# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("🎥 Video Settings")

    url = st.text_input("YouTube URL")

    if st.button("Load Video"):

        with st.spinner("Processing video..."):

            video_id = extract_video_id(url)

            transcript = get_transcript(video_id)

            chunks = create_chunks(transcript)

            vector_store = create_vector_store(chunks)

            retriever = create_retriever(vector_store)

            set_retriever(retriever)

            st.session_state.retriever = retriever

        st.success("Video Loaded Successfully!")

# -----------------------------
# Display Chat History
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------

prompt = st.chat_input(
    "Ask anything from the video:"
)

if prompt:

    if st.session_state.retriever is None:

        st.error(
            "Please load a YouTube video first."
        )

        st.stop()

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Message
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            config = {
                "configurable": {
                "thread_id": "1"
               }
            }

            result = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(content=prompt)
                    ]
                },
                config = config,
            )

            answer = result["messages"][-1].content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )