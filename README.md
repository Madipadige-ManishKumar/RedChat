# Redchat

**Redchat** is an intelligent, multi-tool Slack agent designed to act as a friendly and knowledgeable academic peer. It leverages the **Google Gemini** model to orchestrate complex tasks including searching through Slack history via **Retrieval-Augmented Generation (RAG)**, managing **GitHub** repositories, and communicating across Slack channels.

---

## 📂 Project Structure

```text
.
├── chromeDB/               # Persistent vector database storage
├── src/
│   ├── agents/
│   │   ├── executor.py     # Core agent logic and Gemini tool loop
│   │   ├── tools.py        # Definitions for Slack, GitHub, and RAG tools
│   │   └── prompts.py      # System instructions and prompt templates
│   ├── MCP/
│   │   └── Github/
│   │       └── service.py  # GitHub API integrations for repos and issues
│   ├── rag/
│   │   ├── ingest.py       # Logic for embedding Slack history into ChromaDB
│   │   └── reteriver.py    # Vector database querying and RAG retrieval
│   ├── slack/
│   │   ├── client.py       # Slack client and Bolt app initialization
│   │   └── service.py      # Functions for messaging and history retrieval
│   ├── utilis/
│   │   └── reset_db.py     # Utility to clear the local vector database
│   ├── config.py           # Configuration and environment variable management
│   └── main.py             # Entry point for the Slack Socket Mode app
├── .env                    # Local environment variables (ignored by git)
└── requirements.txt        # Project dependencies

```

---

## 🛠️ Technologies

* **LLM:** Google Gemini (`gemini-3-flash-preview`).
* **Orchestration:** Function calling and automated tool loops via the Gemini Python SDK.
* **Vector Database:** **ChromaDB** for storing and retrieving Slack context.
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2` for semantic search.
* **Slack SDK:** Slack Bolt and WebClient for real-time interaction.
* **GitHub API:** PyGithub for automated repository and issue management.

---

## ⚙️ Setup

### 1. Environment Variables

Create a `.env` file in the root directory with the following keys:

```ini
apikey="Enter the Value"
slack_outh_token="Enter the Value"
slack_app_token="Enter the Value"
github_token="Enter the Value"

```

* **apikey**: Your Google Gemini API Key.
* **slack_outh_token**: Slack Bot User OAuth Token.
* **slack_app_token**: Slack App-level Token for Socket Mode.
* **github_token**: GitHub Personal Access Token.

### 2. Run the Application

Start the Slack agent using the following command:

```bash
python -m src.main

```

---

## 🚀 Key Features

* **Semantic Slack Search:** Uses semantic chunking to understand and retrieve information from previous Slack conversations.
* **GitHub Integration:** Allows the agent to create repositories and open issues directly from Slack prompts.
* **Channel Awareness:** Can fetch history from or post messages to specific channels or all joined channels.
* **Natural Responses:** The agent is instructed to avoid robotic phrasing like "Based on the text" and provide direct, helpful answers.
