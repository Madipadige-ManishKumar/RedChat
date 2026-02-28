import time
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import CHROME_PATH,EMBEDDING_MODEL
from src.slack  import get_all_joined_channels_history
from langchain_experimental.text_splitter import SemanticChunker
from src.slack.service import get_channel_id_by_name,fetch_history


def embedding_for_channels(channel_names: list):
    combined_report = ""
    for name in channel_names:
        c_id = get_channel_id_by_name(name)
        if c_id:
            history = fetch_history(c_id, limit=50)
            combined_report += f"\n--- RECENT MESSAGES FROM {name} ---\n{history}\n"
        else:
            combined_report += f"\n--- Could not find channel: {name} ---\n"
    
    if not combined_report.strip():
        print("No data to embed from Slack.")
        return
    
    doc = Document(page_content = combined_report,
    metadata={"source": "slack","timestamp": time.time()})
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    semantic_chunker = SemanticChunker(embeddings,breakpoint_threshold_type="percentile")
    docs = [Document(page_content=combined_report,metadata={"source": "slack","timestamp": time.time()})]
    semantic_chunks = semantic_chunker.split_documents(docs)

    vector_store = Chroma(
        persist_directory=CHROME_PATH,
        embedding_function=embeddings
    )
    vector_store.add_documents(semantic_chunks)
    print(f"Embedded {len(semantic_chunks)} chunks into the vector database.")


def ingest_slack_to_rag():
    slack_data = get_all_joined_channels_history()
    if not slack_data or "I am not in any channels" in slack_data:
        print("No data to ingest from Slack.")
        return
    doc = Document(page_content = slack_data,
    metadata={"source": "slack","timestamp": time.time()})
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    semantic_chunker = SemanticChunker(embeddings,breakpoint_threshold_type="percentile")
    docs = [Document(page_content=slack_data,metadata={"source": "slack","timestamp": time.time()})]
    semantic_chunks = semantic_chunker.split_documents(docs)

    vector_store = Chroma(
        persist_directory=CHROME_PATH,
        embedding_function=embeddings
    )
    vector_store.add_documents(semantic_chunks)
    print(f"Ingested {len(semantic_chunks)} chunks into the vector database.")


if __name__ == "__main__":
    ingest_slack_to_rag()