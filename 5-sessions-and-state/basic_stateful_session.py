"""
This script demonstrates basic stateful session management using the Google ADK.
It initializes an in-memory session service, creates a session with an initial state
(user name and preferences), and then uses a runner to interact with a
question-answering agent. The script sends a message to the agent and prints
the agent's final response. Finally, it retrieves and prints the session's state
to show how it's maintained.
"""

import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent
from rich import print


load_dotenv()

# Create a new in-memory session service to store the session state.
# For production, a persistent store like FirestoreSessionService would be used.
session_service_stateful = InMemorySessionService()

# Define the initial state for the session.
# This data will be available to the agent during its interactions.
initial_state = {
    "user_name": "Rod Morrison",
    "user_preferences": """
        I like Jujutsu, I like to play chess, and I like to play video games.
        My favorite food is pizza.
        My favorite TV show is The Office.
        Like when people collaborate with with him.
    """,
}

# Define constants for session identification.
APP_NAME = "Rod Bot"
USER_ID = "rod_morrison"
SESSION_ID = str(uuid.uuid4())  # Generate a unique session ID

# Create a new session with the defined initial state.
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

print("=== Created a new session ===")
print(f"\tSession ID: {SESSION_ID}")

# Create a new runner to manage interactions with the agent.
# The runner is configured with the agent, app name, and the session service.
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

# Prepare a new message to send to the agent.
new_message = types.Content(
    role="user", parts=[types.Part(text="What are my preferences?")]
)

# Send the message to the agent and process the events.
# The runner handles the communication with the agent and manages the session.
print("=== Sending message to agent and processing response ===")
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

# Retrieve the session from the session service to inspect its state.
print("=== Session Event Exploration ===")
session = session_service_stateful.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

# Log the final session state to observe any changes or confirm persistence.
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"\t{key}: {value}")
