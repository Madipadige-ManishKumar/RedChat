import os
from typing import List, Dict
from dotenv import load_dotenv

# Slack Bolt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

load_dotenv()


BOT_TOKEN = os.getenv("slack_outh_token")
APP_TOKEN = os.getenv("slack_app_token")
API_KEY = os.getenv("apikey")


chat_history_store: Dict[str, List] = {}

def get_history(channel_id: str) -> List:
    if channel_id not in chat_history_store:
        chat_history_store[channel_id] = []
    return chat_history_store[channel_id]


def initialize_conversational_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma(
        persist_directory="./chroma_db", 
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=API_KEY,
        temperature=0.7 # Increased slightly for more natural variety
    )
    contextualize_q_system_prompt = (
        "Given the chat history and a new question, make it a standalone question "
        "that can be understood without history. Do not answer it yet."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    system_prompt = (
        "You are a friendly and knowledgeable academic peer. "
        "Answer the question naturally using the provided context. "
        "CRITICAL RULES: "
        "1. DO NOT say 'Based on the provided text', 'According to the documents', or 'Reference 1 says'. "
        "2. Just answer the question directly as if you already knew the information. "
        "3. If you don't know, just guide the user based on general knowledge or ask for clarification. "
        "4. Maintain an encouraging, non-robotic tone.\n\n"
        "5. Answer the question using only the information from the retrieved documents. Do not use any outside knowledge. "
        "Context: {context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)
    return create_retrieval_chain(history_aware_retriever, combine_docs_chain)

# 3. Slack Event Handling
app = App(token=BOT_TOKEN)
rag_chain = initialize_conversational_rag()

@app.event("app_mention")
def handle_mention(event, say):
    channel_id = event['channel']
    user_query = event['text'].split(">")[-1].strip()
    
    history = get_history(channel_id)
    
    try:
        # Run the chain
        response = rag_chain.invoke({
            "input": user_query, 
            "chat_history": history
        })
        
        answer = response["answer"]
        
        # Update memory for the next turn
        history.append(HumanMessage(content=user_query))
        history.append(AIMessage(content=answer))
        chat_history_store[channel_id] = history[-6:]
        
        say(text=answer)
        
    except Exception as e:
        print(f"Error: {e}")
        say(text="Hey, I hit a snag while thinking. Can you try asking that again?")

if __name__ == "__main__":
    handler = SocketModeHandler(app, APP_TOKEN)
    print(" Conversational  RAG on Slack!")
    handler.start()