import streamlit as st
from app.chatbot import chatbot
from langchain_core.messages import HumanMessage

from app.transcript import (
    extract_video_id,
    get_transcript,
)

from app.retrieval import (
    create_chunks,
    create_vector_store,
    create_retriever,
)

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="YouTube Agentic RAG",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Google Font
# --------------------------------------------------

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Global */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App */

.stApp {
    background-color: #000000;
}

/* Main Area */

.block-container {
    max-width: 1200px;
    padding-top: 1rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #222222;
}

/* Chat Input */

[data-testid="stChatInput"] {
    background-color: #111111;
}

[data-testid="stChatInput"] textarea {
    font-size: 18px !important;
    min-height: 70px;
    color: white !important;
}

/* Messages */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
}

/* Response Text */

[data-testid="stMarkdownContainer"] {
    font-size: 18px;
    line-height: 1.8;
}

/* Buttons */

.stButton button {
    border-radius: 18px;
    background-color: #111111;
    border: 1px solid #333333;
    color: white;
    font-weight: 600;
}

/* Hide Streamlit Branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:


    st.divider()

    url = st.text_input(
        "YouTube URL",
        placeholder="Paste YouTube URL..."
    )

    load_video = st.button(
        "🚀 Load Video",
        use_container_width=True,
    )

    st.divider()

    

# --------------------------------------------------
# Load Video
# --------------------------------------------------

if load_video:

    status_placeholder = st.sidebar.empty()

    status_placeholder.info(
        "⏳ Processing video..."
    )

    try:

        video_id = extract_video_id(url)

        transcript = get_transcript(video_id)

        chunks = create_chunks(transcript)

        vector_store = create_vector_store(chunks)

        retriever = create_retriever(
                vector_store
            )

        st.session_state.retriever = retriever

        
        print("Retriever successfully set.")

        st.session_state.chunk_count = len(chunks)

        status_placeholder.success(
            "✅ Video Loaded"
        )

        st.rerun()

    except Exception as error:

        st.error(f"Error: {error}")

# --------------------------------------------------
# Landing Screen
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div style="
        text-align:center;
        padding-top:40px;
        padding-bottom:40px;
    ">

    <h1 style="
        font-size:56px;
        font-weight:800;
        margin-bottom:10px;
    ">
    🎥 YouTube Agentic RAG
    </h1>

    <p style="
        font-size:22px;
        color:#999999;
    ">
    Chat with any YouTube video
    </p>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Starter Prompts
# --------------------------------------------------

if (
    len(st.session_state.messages) == 0
    and st.session_state.retriever is not None
):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        summarize_clicked = st.button(
            "📄 Summarize",
            use_container_width=True,
        )

    with col2:
        concepts_clicked = st.button(
            "🎯 Concepts",
            use_container_width=True,
        )

    with col3:
        notes_clicked = st.button(
            "📝 Notes",
            use_container_width=True,
        )

    with col4:
        quiz_clicked = st.button(
            "❓ Quiz",
            use_container_width=True,
        )

    starter_prompt = None

    if summarize_clicked:
        starter_prompt = "Summarize this video."

    elif concepts_clicked:
        starter_prompt = "What are the key concepts discussed in this video?"

    elif notes_clicked:
        starter_prompt = "Generate detailed study notes from this video."

    elif quiz_clicked:
        starter_prompt = "Create a quiz based on this video."

    if starter_prompt:

        with st.spinner("Thinking..."):

            result = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(content=starter_prompt)
                    ]
                },
                config={
                   "configurable": {
                   "thread_id": "youtube_chat"
                },

                   "retriever": st.session_state.retriever
                },
            )

            answer = result["messages"][-1].content

        st.session_state.messages.append(
            {
                "role": "user",
                "content": starter_prompt,
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        st.rerun()

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

# --------------------------------------------------
# Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🎥"

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask anything about the video..."
)

if prompt:

    if st.session_state.retriever is None:

        st.error(
            "Please load a YouTube video first."
        )

        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message(
        "user",
        avatar="👤",
    ):
        st.markdown(prompt)

    with st.chat_message(
        "assistant",
        avatar="🎥",
    ):

        with st.spinner("Thinking..."):

            result = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(content=prompt)
                    ]
                },
                config={
                   "configurable": {
                   "thread_id": "youtube_chat"
                },

                   "retriever": st.session_state.retriever
                },
            )

            answer = result["messages"][-1].content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.rerun()