from app.retrieval import (
    create_chunks,
    create_vector_store,
    create_retriever,
)

from app.chatbot import (
    chatbot,
    set_retriever,
)

from langchain_core.messages import HumanMessage


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

        set_retriever(retriever)

        print("Retriever ready.\n")

        print("You can now chat with the video.")
        
        print("Type 'exit' to quit.\n")

        while True:

            question = input("You: ")

            if question.lower() == "exit":
                break

            config = {
                "configurable": {
                    "thread_id": "terminal_chat"
                }
            }

            result = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(content=question)
                    ]
                },
                config=config,
            )

            answer = result["messages"][-1].content

            print("\nAI:", answer)
            print()

    except Exception as error:

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()