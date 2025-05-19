import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent
from rich import print


load_dotenv()

# Create a new session service to store the session state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Rod Morrison",
    "user_preferences": """
        I like Jujutsu, I like to play chess, and I like to play video games.
        My favorite food is pizza.
        My favorite TV show is The Office.
        Like when people collaborate with with him.
    """
}

# Create a New Session
APP_NAME = "Rod Bot"
USER_ID = "rod_morrison"
SESSION_ID = str(uuid.uuid4())

stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

print("=== Created a new session ===")
print(f"\tSession ID: {SESSION_ID}")

# Create a new runner
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What are my preferences?")]
)

# Send a message to the agent
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")
            
# Print the session state
print("=== Session Event Exploration ===")
session = session_service_stateful.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

# Log the final session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"\t{key}: {value}")