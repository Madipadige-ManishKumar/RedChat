from src.config import SLACK_BOT_TOKEN
from src.slack.client import client  

def get_channel_id_by_name(name: str):
    try:
        clean_name = name.lstrip('#')
        response = client.conversations_list()

        for channel in response["channels"]:
            if channel["name"] == clean_name:
                return channel["id"]
        return None
    except Exception as e:
        return f"Error finding channel: {e}"


def fetch_history(channel_id: str, limit: int = 20):
    try:
        result = client.conversations_history(channel=channel_id, limit=limit)
        messages = result["messages"]
        # Format for LLM context
        formatted = [f"User {m.get('user')}: {m.get('text')}" for m in messages[::-1]]
        return "\n".join(formatted)
    except Exception as e:
        return f"Error fetching history: {e}"

def get_multiple_channels_history(channel_names: list, limit_per_channel: int = 20):

    combined_report = ""
    for name in channel_names:
        c_id = get_channel_id_by_name(name)
        if c_id:
            history = fetch_history(c_id, limit=limit_per_channel)
            combined_report += f"\n--- RECENT MESSAGES FROM {name} ---\n{history}\n"
        else:
            combined_report += f"\n--- Could not find channel: {name} ---\n"
    return combined_report
def get_all_joined_channels():
    try:
        response = client.conversations_list()
        joined_channels = [c for c in response["channels"] if c.get("is_member")]
        return joined_channels
    except Exception as e:
        return f"Error fetching all channels: {e}"
def get_all_joined_channels_history(limit_per_channel: int = 15):
    try:
        
        response = client.conversations_list()
        # print(response,"This is the reponse in the function get_all_joined_channels_history")
        joined_channels = [c for c in response["channels"] if c.get("is_member")]
        # print(joined_channels,"")
        
        all_history = ""
        for channel in joined_channels:
            history = fetch_history(channel["id"], limit=limit_per_channel)
            all_history += f"\n--- CHANNEL: {channel['name']} ---\n{history}\n"
        
        return all_history if all_history else "I am not in any channels yet."
    except Exception as e:
        return f"Error fetching all channels: {e}"
def post_to_all_channels(text: str):
    try:
        response = client.conversations_list()
        joined_channels = [c for c in response["channels"] if c.get("is_member")]
        for channel in joined_channels:
            client.chat_postMessage(channel=channel["id"], text=text)
        return "Sent to all channels."
    except Exception as e:
        return f"Error posting to all channels: {e}"
def post_to_multiple_channels(channel_names: list, text: str):
    # print("Posting to multiple channels:", channel_names, text)
    results = []
    for name in channel_names:
        c_id = get_channel_id_by_name(name)
        # print(f"Channel: {name}, ID: {c_id}")
        if c_id:
            try:
                client.chat_postMessage(channel=c_id, text=text)
                results.append(f"Sent to {name}")
            except Exception as e:
                results.append(f"Failed {name}: {e}")
        else:
            results.append(f"❓ Channel {name} not found.")
    return "\n".join(results)



    # Quick test
    # print(get_all_joined_channels_history())
    # print(get_channel_id_by_name("#general"))
    # print(fetch_history(get_channel_id_by_name("#general")))