from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def load_documents(markdown_path: str|Path) -> list[Document]:
    """
    Create Document objects from a markdown file containing FAQ content.
    
    :param markdown_path: Path to the markdown file containing the FAQ content.
    :type markdown_path: str | Path
    :return: A list of Document objects, each representing a question-answer pair along with its category and metadata.
    :rtype: list[Document]
    """
    text = Path(markdown_path).read_text(encoding="utf-8")

    blocks = [block.strip() for block in text.split("---") if block.strip()]

    documents = []
    current_category = None

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if not lines:
            continue

        # Skip title
        if lines[0].startswith("# The Clothing Store"):
            continue

        # Update current category
        if lines[0].startswith("# "):
            current_category = lines[0][2:].strip()
            lines = lines[1:]

        if not lines:
            continue

        # Extract question
        question = lines[0].replace("## ", "").strip()

        # Extract answer
        answer = "\n".join(lines[1:]).strip()

        documents.append(
            Document(
                page_content=f"""Category: {current_category}

Question: {question}

Answer:
{answer}""",
                metadata={
                    "category": current_category,
                    "question": question,
                    "question_no": question[:2],
                    "answer": answer,
                    "source": "The Clothing Store FAQ",
                },
            )
        )

    return documents


def store_documents(documents: list[Document], chroma_db_directory: str | Path, collection_name: str) -> Chroma:
    """
    Store a list of Document objects in a Chroma vector store.
    
    :param documents: A list of Document objects to be stored in the Chroma vector store.
    :type documents: list[Document]
    :param chroma_db_directory: The directory where the Chroma vector store will be persisted.
    :type chroma_db_directory: str | Path
    :return: A Chroma vector store instance containing the embedded documents.
    :rtype: Chroma
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=chroma_db_directory,
        collection_name=collection_name,
    )

    return vectorstore

if __name__ == "__main__":

    markdown_path = Path("data/clothing_store_faq.md")

    documents = load_documents(markdown_path)

    vectorstore = store_documents(documents, chroma_db_directory="vector_store", collection_name="clothing_store_faq")

    print(f"Stored {len(documents)} documents in ChromaDB.")