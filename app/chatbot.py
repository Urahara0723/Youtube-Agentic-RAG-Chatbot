from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages #add_message is more optimized to work with Basemessages.
from app.config import llm
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import PromptTemplate
from app.prompts import SUMMARY_PROMPT


class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]
    context: str

CURRENT_RETRIEVER = None

def set_retriever(retriever):
    global CURRENT_RETRIEVER
    CURRENT_RETRIEVER = retriever

def retrieve_node(state: ChatState):

    question = state["messages"][-1].content

    docs = CURRENT_RETRIEVER.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {
        "context": context
    }

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

def chat_node(state: ChatState):

    question = state["messages"][-1].content

    context = state["context"]

    prompt = PromptTemplate(
        template=SUMMARY_PROMPT,
        input_variables=[
            "context",
            "question",
        ],
    )

    final_prompt = prompt.format(
        context=context,
        question=question,
    )

    response = llm.invoke(
        final_prompt
    )

    return {
        "messages": [response]
    }

# adding nodes
graph.add_node(
    "retrieve_node",
    retrieve_node
)

graph.add_node(
    "chat_node",
    chat_node
)

graph.add_edge(
    START,
    "retrieve_node"
)

graph.add_edge(
    "retrieve_node",
    "chat_node"
)

graph.add_edge(
    "chat_node",
    END
)

chatbot = graph.compile(checkpointer= checkpointer)

