# Google ADK: Persistent Storage Agent

This project demonstrates how to build a stateful agent using the Google Agent Development Kit (ADK) that can remember information across conversations by leveraging persistent storage. The agent, named "Memory Agent," can manage user reminders and remember the user's name.

## Key Features

*   **Persistent Sessions**: Uses `DatabaseSessionService` from the Google ADK to store session state in an SQLite database (`my_agent_data.db`). This allows the agent to recall information from previous interactions with the same user.
*   **Tool-Based Functionality**: The agent is equipped with several tools:
    *   `add_reminder`: Adds a new reminder to the user's list.
    *   `view_reminders`: Displays all current reminders.
    *   `update_reminder`: Modifies an existing reminder by its index.
    *   `delete_reminder`: Removes a reminder by its index.
    *   `update_user_name`: Updates the user's name stored in the session.
*   **Stateful Interaction**: The agent's instructions guide it to use the stored `user_name` and `reminders` from the session state to personalize responses and manage tasks.
*   **Interactive Chat**: An asynchronous chat loop in `main.py` allows users to interact with the agent from the command line.
*   **Clear Console Output**: Uses the `rich` library and custom ANSI color codes for enhanced readability of agent interactions, tool calls, and state display in the terminal.

## Project Structure

```
.
├── main.py                 # Main script to run the interactive chat and manage sessions.
├── memory_agent/
│   ├── __init__.py         # Makes the 'memory_agent' a Python package.
│   └── agent.py            # Defines the Memory Agent, its tools, and instructions.
├── utils.py                # Utility functions for displaying session state and processing agent responses.
├── my_agent_data.db        # SQLite database file created to store session data (auto-generated).
└── .env                    # (Optional/Not Pictured) For storing environment variables like API keys.
```

*   **`main.py`**:
    *   Initializes the `DatabaseSessionService` for SQLite.
    *   Manages session creation: finds an existing session for the user or creates a new one with an initial state.
    *   Sets up the ADK `Runner` with the `memory_agent`.
    *   Contains the main asynchronous interactive chat loop.
*   **`memory_agent/agent.py`**:
    *   Defines the core tool functions (`add_reminder`, `view_reminders`, etc.) that interact with the `tool_context.state` to modify session data.
    *   Instantiates the `Agent` (named `memory_agent`) with its model, description, detailed instructions for behavior and tool usage, and registers the tool functions.
*   **`utils.py`**:
    *   `Colors`: A class for ANSI escape codes to color terminal output.
    *   `display_state`: A function to fetch and print the current session state (user name and reminders) in a formatted way.
    *   `process_agent_response`: Handles and prints various events from the agent's execution flow (tool calls, tool responses, final agent text).
    *   `call_agent_async`: Orchestrates sending a user query to the agent via the `Runner`, displaying state before and after, and processing the asynchronous stream of events.

## How to Run

1.  **Prerequisites**:
    *   Python 3.x
    *   Install required Python packages:
        ```bash
        pip install google-generativeai python-dotenv rich
        # Or if using Vertex AI models:
        # pip install google-cloud-aiplatform python-dotenv rich
        ```
        (The Google ADK itself is typically included via `google-generativeai` or `google-cloud-aiplatform` depending on the models you intend to use with `LiteLlm` or `VertexAIModel` respectively. Your `memory_agent` uses `gemini-2.0-flash` which implies `google-generativeai`.)

2.  **Environment Variables**:
    *   Ensure you have the necessary API keys for the LLM service you are using (e.g., `GOOGLE_API_KEY` for Gemini models via `google-generativeai`).
    *   You can place these in a `.env` file in the project root, which `python-dotenv` will load. Example `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

3.  **Execute the Main Script**:
    ```bash
    python main.py
    ```

4.  **Interact with the Agent**:
    *   The script will welcome you to the Memory Agent Chat.
    *   Type your requests (e.g., "What's my name?", "Add a reminder to buy milk", "Show my reminders", "My name is Alex").
    *   Type "exit" or "quit" to end the chat. Session data will be persisted in `my_agent_data.db`.

## Example Interactions

```
User: What's my name?
Agent: Your name is Rod Morrison.

User: Add a reminder: Call John at 5 PM
Agent: OK, Rod, I've added "Call John at 5 PM" to your reminders.

User: Show reminders
Agent:
📝 Reminders:
  1. Call John at 5 PM

User: My name is David
Agent: Okay, I've updated your name to David.
```

Upon restarting the script, the agent will remember "David" as the user's name and any previously added reminders.