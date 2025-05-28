# Google ADK: Multi-Agent System Example

This project demonstrates how to build a hierarchical multi-agent system using the Google Agent Development Kit (ADK). It features a `manager` agent that orchestrates tasks by delegating to specialized sub-agents or utilizing specific tools.

## Key Features

*   **Hierarchical Agent Structure**: A `manager` agent acts as the primary interface and decision-maker.
*   **Task Delegation**: The `manager` agent is instructed to delegate tasks to appropriate sub-agents based on the user's query.
*   **Specialized Sub-Agents**:
    *   **`stock_analyst`**: Fetches current stock prices using the `yfinance` library.
    *   **`news_analyst`**: Searches for news articles using Google Search and can use the current time to refine queries.
    *   **`funny_nerd`**: Tells topic-based jokes and remembers the last joke topic.
*   **Agent as a Tool**: The `news_analyst` sub-agent is used as a tool by the `manager` agent, showcasing how agents can be composed.
*   **Standard Tools**: The `manager` agent also has direct access to a `get_current_time` tool.
*   **Stateful Sub-Agent**: The `funny_nerd` agent demonstrates simple statefulness by remembering the last topic a joke was told about.

## Project Structure

The `7-multi-agent` directory is structured as follows:

```
7-multi-agent/
├── manager/
│   ├── __init__.py
│   ├── agent.py            # Defines the root 'manager' agent and its configuration.
│   ├── sub_agents/
│   │   ├── __init__.py
│   │   ├── funny_nerd/
│   │   │   ├── __init__.py
│   │   │   └── agent.py    # Defines the 'funny_nerd' sub-agent and its joke tool.
│   │   ├── news_analyst/
│   │   │   ├── __init__.py
│   │   │   └── agent.py    # Defines the 'news_analyst' sub-agent (uses Google Search).
│   │   └── stock_analyst/
│   │       ├── __init__.py
│   │       └── agent.py    # Defines the 'stock_analyst' sub-agent and its stock price tool.
│   └── tools/
│       ├── __init__.py
│       └── tools.py        # Defines common tools like 'get_current_time'.
├── main.py                 # Main script to run the interactive chat with the multi-agent system.
├── .env                    # (Optional) For environment variables like API keys.
└── README.md               # This file.
```

*   **`manager/agent.py`**: Defines the `root_agent` (the manager). It lists `stock_analyst` and `funny_nerd` as `sub_agents` for delegation and `news_analyst` (wrapped in `AgentTool`) and `get_current_time` as its direct `tools`.
*   **`manager/sub_agents/*/agent.py`**: Each file defines a specialized agent with its own instructions, model, and tools.
*   **`manager/tools/tools.py`**: Contains utility tool functions.
*   **`main.py`**: Initializes the ADK `Runner` with the `manager.agent.root_agent` and provides an interactive command-line interface for chatting with the system. It handles session management (though persistence might depend on `DatabaseSessionService` if configured, similar to example `6-persistent-storage`).

## How to Run

1.  **Prerequisites**:
    *   Ensure you have completed the main project setup (Python, `requirements.txt`) as described in the [root README.md](../../README.md).
    *   This example specifically uses `yfinance` for the stock analyst, which is included in the main `requirements.txt`.

2.  **Environment Variables**:
    *   Ensure your main `.env` file (in the project root `Google_Agents/`) is configured with necessary API keys (e.g., `GOOGLE_API_KEY`).
    *   If this example has its own `.env` file (e.g., `7-multi-agent/.env`), ensure it's also correctly set up.

3.  **Navigate to the Directory**:
    ```bash
    cd 7-multi-agent
    ```

4.  **Execute the Main Script**:
    ```bash
    python main.py
    ```

5.  **Interact with the Agent System**:
    *   The script will start an interactive chat session.
    *   You can ask the `manager` agent various questions, and it should delegate to the appropriate sub-agent or use its tools.

## Example Interactions

*   "What's the current price of GOOG?" (Should be delegated to `stock_analyst`)
*   "Tell me a joke about computers." (Should be delegated to `funny_nerd`)
*   "What's the latest news on AI?" (Manager might use `news_analyst` tool)
*   "What time is it?" (Manager might use `get_current_time` tool)

The system will show logs indicating which agent is handling the request and which tools are being called.