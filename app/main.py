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


def main():

    try:

        print("YouTube RAG Chatbot\n")

        url = input("Enter YouTube URL:\n")

        print("\n Fetching transcript...\n")

        video_id = extract_video_id(url)

        transcript = get_transcript(video_id)

        print("Transcript fetched successfully.\n")

        print("Creating embeddings...\n")

        chunks = create_chunks(transcript)

        vector_store = create_vector_store(chunks)

        retriever = create_retriever(vector_store)

        print("Retriever ready.\n")

        question = input("Ask a question about the video:\n")

        print("\n Generating answer...\n")

        answer = generate_answer(retriever, question)

        print("\n AI Response:\n")

        print(answer)

    except Exception as error:

        print(f"\n Error: {error}")


if __name__ == "__main__":
    main()
