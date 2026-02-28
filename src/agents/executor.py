from src.agents.tools import TOOLS
from google import genai 
from google.genai import types
from src.config import GEMINI_API_KEY,MODEL_ID


client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are a friendly and knowledgeable academic peer. Answer the question naturally using the provided context. CRITICAL RULES: 1. DO NOT say 'Based on the provided text', 'According to the documents', or 'Reference 1 says'. 2. Just answer the question directly as if you already knew the information. 3. If you don't know, just guide the user based on general knowledge or ask for clarification. 4. Maintain an encouraging, non-robotic tone.\n\n5. Answer the question using only the information from the retrieved documents. Do not use any outside knowledge. and if you can't answer then say I don't have information regarding that.
"""


def run_agent(user_query: str):
    """
    Main loop that sends a query to Gemini and executes 
    tools if Gemini requests them.
    """
    
    # Define the tools available to the LLM
    # Note: We are only including Slack tools for now as per your request
    

    print(f"🤖 Agent received query: {user_query}")

    # Generate content with tools enabled
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=TOOLS,
            automatic_function_calling={"disable": False} # This handles the loop for you!
        )
    )

    return response.text


# if __name__ == "__main__":
#     # Quick test
#     print(run_agent("send message 'Hello team!' to #test channels and then fetch the recent history of the #general channel"))