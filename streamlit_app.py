import streamlit as st

from app.transcript import (
    extract_video_id,
    get_transcript,
)

from app.rag_pipeline import (
    create_chunks,
    create_vector_store,
    create_retriever,
    generate_answer,
)

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
)

st.title("🎥 YouTube RAG Chatbot")

url = st.text_input("Enter YouTube URL")

question = st.text_input("Ask a question")

if st.button("Generate Answer"):

    with st.spinner("Processing video..."):

        video_id = extract_video_id(url)

        transcript = get_transcript(video_id)

        chunks = create_chunks(transcript)

        vector_store = create_vector_store(chunks)

        retriever = create_retriever(vector_store)

        answer = generate_answer(retriever, question)

    st.success("Answer Generated!")

    st.write(answer)
