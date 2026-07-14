from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder="./cache"
    )

vectorstore = Chroma(
    persist_directory="vector_store",
    embedding_function=embeddings,
    collection_name="clothing_store_faq",
)

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", cache_folder="./cache")

def get_relevant_documents(query, top_k=8):

    cat = ["RETURNS, EXCHANGE & REFUND","ORDERS & PAYMENT", "SHIPPING & TRACKING"]

    docs: list[Document] = []
    
    for c in cat:
        docs += vectorstore.similarity_search(query, k=5, filter={"category": c}) # Retrieve 5 docs for each category

    # Reranking
    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, docs), reverse=True)
    final_docs = [doc for _, doc in ranked[:top_k]]

    return final_docs