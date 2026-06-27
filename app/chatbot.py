from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_core.prompts import PromptTemplate

from app.config import llm
from app.prompts import SUMMARY_PROMPT


# --------------------------------------------------
# State
# --------------------------------------------------

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

    search_query: str

    context: str



# --------------------------------------------------
# Query Understanding
# --------------------------------------------------

def understand_query_node(state: ChatState):

    messages = state["messages"]

    latest_question = messages[-1].content

    history = "\n".join(

        f"{type(msg).__name__}: {msg.content}"

        for msg in messages[:-1]

    )

    prompt = f"""
You are a Query Understanding Agent.

Conversation History:

{history}

Current User Question:

{latest_question}

Rewrite the user's question into a standalone search query.

Rules:

- Resolve references like:
    - it
    - this
    - that
    - first point
    - second topic
    - previous answer

- If the question is already standalone,
return it unchanged.

Return ONLY the search query.
"""

    response = llm.invoke(

        [
            SystemMessage(content=prompt)
        ]

    )

    search_query = response.content.strip()

    print("\n========== QUERY ==========")
    print(search_query)
    print("===========================\n")

    return {

        "search_query": search_query

    }


# --------------------------------------------------
# Retrieval
# --------------------------------------------------

def retrieve_node(state: ChatState, config):

    retriever = config["configurable"]["retriever"]

    query = state["search_query"]

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {
        "context": context
    }

# --------------------------------------------------
# Generation
# --------------------------------------------------

def generate_node(state: ChatState):

    question = state["messages"][-1].content

    context = state["context"]

    prompt = PromptTemplate(

        template=SUMMARY_PROMPT,

        input_variables=[

            "context",

            "question",

        ],

    )

    system_prompt = prompt.format(

        context=context,

        question=question,

    )

    conversation = [

        SystemMessage(content=system_prompt)

    ]

    conversation.extend(

        state["messages"]

    )

    print("\n========== MEMORY ==========")

    for msg in state["messages"]:

        print(type(msg).__name__, ":", msg.content)

    print("============================\n")

    response = llm.invoke(conversation)

    return {

        "messages": [

            AIMessage(content=response.content)

        ]

    }


# --------------------------------------------------
# Graph
# --------------------------------------------------

graph = StateGraph(ChatState)

graph.add_node(

    "understand_query",

    understand_query_node,

)

graph.add_node(

    "retrieve",

    retrieve_node,

)

graph.add_node(

    "generate",

    generate_node,

)

graph.add_edge(

    START,

    "understand_query",

)

graph.add_edge(

    "understand_query",

    "retrieve",

)

graph.add_edge(

    "retrieve",

    "generate",

)

graph.add_edge(

    "generate",

    END,

)


memory = MemorySaver()

chatbot = graph.compile(

    checkpointer=memory

)