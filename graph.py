from typing import Annotated, TypedDict

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from prompts import SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)


# Vector Store
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="vector_store",
    embedding_function=embeddings,
    collection_name="clothing_store_faq",
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 7}
)


# State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    documents: list[Document]


# Nodes
def retrieve(state: State):

    question = state["messages"][-1].content

    docs = retriever.invoke(question)

    return {
        "documents": docs,
    }

def generate(state: State):

    context = "\n\n".join([doc.page_content for doc in state["documents"]])

    system_prompt = SYSTEM_PROMPT.format(context)

    response = llm.invoke(
        [
            ("system", system_prompt),
            *state["messages"],
        ]
    )

    return {
        "messages": [AIMessage(content=response.content[0]["text"])],
    }


# Graph
builder = StateGraph(State)

builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile(checkpointer=InMemorySaver())

chatbot = graph

    