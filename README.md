# The Clothing Store - Customer Support Chatbot

Streamlit-based customer support chatbot for a clothing store. The app uses a retrieval-augmented generation (RAG) workflow to answer questions about orders, shipping, and returns.

## Demo

Streamlit app URL: \
https://customer-support-rag--llm-langchain-langgraph-gemini-app-befpl.streamlit.app/

![Project 1 Demo](src/CustomerSupportRAG_Demo.gif)


# Workflow

## 1. Knowledge Base

A synthetic FAQ knowledge base was created for a fictional clothing company called **The Clothing Store (TCS)**.

The knowledge base is stored as a Markdown file containing customer support information related to:

- Orders & Payment
- Shipping & Tracking
- Returns, Exchange & Refund

---

## 2. Document Ingestion

The Markdown knowledge base is parsed into structured LangChain `Document` objects.

Each FAQ is stored as an individual document with:

### Metadata

- Category
- Question
- Source

### Content

```
Category

Question

Answer
```

This allows every FAQ to be independently retrieved.

---

## 3. Vector Database

The structured documents are embedded using

**sentence-transformers/all-MiniLM-L6-v2**

and stored in a local **ChromaDB** vector database.

---

## 4. LangGraph Workflow

The chatbot is implemented using a simple LangGraph workflow consisting of two nodes.

### Retrieve Node

- Retrieves the top relevant FAQ documents from ChromaDB.

### Generate Node

- Uses Gemini 3.1 Flash Lite.
- Receives:
  - Retrieved documents
  - Conversation history
- Generates a grounded response with source citations.

Conversation history is maintained using LangGraph message state, allowing the assistant to answer follow-up questions naturally.

---

## 5. Streaming

Responses are streamed token-by-token from LangGraph to the Streamlit frontend, providing a responsive chat experience.

---

# Project Structure

```
.
├── data/
│   └── souled_store_faq.md
│
├── vector_store/
│   └── Chroma Database
│
├── app.py             # Streamlit frontend
├── graph.py           # LangGraph workflow
├── ingest.py          # Markdown → Documents → ChromaDB
├── main.py            # Application entry
├── prompts.py         # System prompt
├── styles.py          # Streamlit styling
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Google Gemini 3.1 Flash Lite
- ChromaDB
- sentence-transformers/all-MiniLM-L6-v2
- Streamlit

---

## Setup

### 1. Install dependencies

```bash
pip install uv
uv sync
```

### 2. Configure environment variables

Do not commit API keys directly to the repository. Use environment variables or a local `.env` file.

Create a `.env` file with:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

You can use `.env.example` as a reference.

### 3. Run the app

```bash
streamlit run app.py
```

## Live Hosted App URL

Replace this with your deployed Streamlit app link:

https://customer-support-rag--llm-langchain-langgraph-gemini-app-befpl.streamlit.app/

## Testing Instructions

- Open the Streamlit app in your browser.
- Ask questions related to orders, shipping, or returns.
- If the app is connected to the correct Google API key and vector store, it should answer using the stored support knowledge.

## Submission Notes

- The repository includes a dependency file: `pyproject.toml` and `uv.lock`.
- API keys are not stored in the repository.
- The project uses `.env` / environment variables for local setup.
