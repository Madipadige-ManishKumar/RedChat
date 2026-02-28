import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. LOAD ENVIRONMENT
load_dotenv()
apikey = os.getenv("apikey")

if not apikey:
    print("Error: 'apikey' not found in your .env file.")
    sys.exit(1)

# =========================================================
# 2. THE TOOLS (Action)
# =========================================================

def search_internal_docs(query: str):
    """Retrieves HR policy information."""
    knowledge_base = {
        "vacation": "Employees get 20 days of PTO per year.",
        "remote work": "The company allows working from home 3 days a week."
    }
    # This print confirms the function was triggered
    print(f"      >> EXECUTION: Searching docs for '{query}'...")
    for key, content in knowledge_base.items():
        if key in query.lower():
            return {"result": content}
    return {"error": "No documentation found."}

def add_numbers(a: float, b: float):
    """Performs addition."""
    print(f"      >> EXECUTION: Adding {a} + {b}...")
    return {"sum": a + b}

# =========================================================
# 3. THE ORCHESTRATOR (The Loop)
# =========================================================

def run_gemini_agent(user_prompt: str, api_key: str):
    client = genai.Client(api_key=api_key)
    # Ensure you use a valid model name
    model_id = "gemini-2.5-flash" 

    chat = client.chats.create(
        model=model_id,
        config=types.GenerateContentConfig(
            tools=[search_internal_docs, add_numbers],
            system_instruction="You are a helpful assistant. Follow the Thought-Action-Observation loop."
        )
    )

    print(f"\n[USER]: {user_prompt}")
    print("="*60)

    # Turn 1
    response = chat.send_message(user_prompt)

    while True:
        # The 'candidate' is the current state of the AI's response
        candidate = response.candidates[0]
        
        # 1. THOUGHT: Did the model provide reasoning text?
        thought = "".join([part.text for part in candidate.content.parts if part.text]).strip()
        if thought:
            print(f"\n[THOUGHT]: {thought}")
        else:
            print("\n[THOUGHT]: (The model is proceeding directly to action...)")

        # 2. ACTION: Identify the tool calls
        tool_calls = [part.function_call for part in candidate.content.parts if part.function_call]

        if not tool_calls:
            # If no more tool calls, we have reached the Final Answer
            print(f"\n[FINAL ANSWER]:\n{response.text}")
            break

        tool_responses = []
        for call in tool_calls:
            print(f"[ACTION]: Calling tool '{call.name}' with args: {call.args}")
            
            # Execute the local function
            if call.name == "search_internal_docs":
                observation = search_internal_docs(**call.args)
            elif call.name == "add_numbers":
                observation = add_numbers(**call.args)
            else:
                observation = {"error": "Unknown tool"}

            # 3. OBSERVATION: Print the result of the tool
            print(f"[OBSERVATION]: {observation}")

            # Prepare the response to send back to the LLM
            tool_responses.append(
                types.Part.from_function_response(name=call.name, response=observation)
            )

        # Pause to respect rate limits
        time.sleep(1)

        # Continue the loop
        print("-" * 30 + " Feeding observations back to AI " + "-" * 30)
        response = chat.send_message(tool_responses)

if __name__ == "__main__":
    query = "How much vacation time do I get, and what is 542.50 plus 123.40?"
    run_gemini_agent(query, apikey)