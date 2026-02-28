from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import CHROME_PATH,EMBEDDING_MODEL
from .ingest import embedding_for_channels
from src.utilis.reset_db import reset_database

def query_vector_db(query:str,channel_names:list,k:int=3):
    '''
     REQUIRED for any 'Search' requests that specify specific channels.
     Used for finding topics, trends, and specific information discussed in the past
     across the specified Slack channels.
    '''
    try:
        print("Querying the Vector DB...")
        embedding_for_channels(channel_names)
        print("Done the embedding for the channels, now accessing the vector database...")
        embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = Chroma(
            persist_directory=CHROME_PATH,
            embedding_function=embedding
        )

        results = vector_store.max_marginal_relevance_search(query,k=k)
        
        if not results:
            return "No relevant information found in the vector database."
        context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
        return context_text

    except Exception as e:
        return f"Error accessing the Vector DB: {str(e)}"


# if __name__ == "__main__":
#     query = "Find me the content realted  to computer networks?"
    
#     print("Printing the content retrived from the vector database: \n",query_vector_db(query))