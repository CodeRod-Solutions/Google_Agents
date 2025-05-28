import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from rich import print
from utils import call_agent_async

load_dotenv()

# === Create a new session service using a database for persistent storage.
# Using SQLite for simplicity, but this can be replaced with any database.
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# === Define the initial state for the session.
# This data will be available to the agent during its interactions.
initial_state = {
    "user_name": "Rod Morrison",
    "reminders": [],
}

async def main_async():
    # Define constants for session identification.
    APP_NAME = "Memory Agent"
    USER_ID = "rod_morrison"
    
    # === Session Management Find or Create Session
    # This will find an existing session or create a new one if it doesn't exist.
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    
    # If there is an existing session, use it; otherwise, create a new one.
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Use the most recent session.
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Using existing session: {SESSION_ID}")
    else:
        # Create a new session with the defined initial state.
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created a new session: {SESSION_ID}")
        
    # === Create a new runner to manage interactions with the agent.
    # Create runner with the memory agent
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    # === Interactive Chat Loop
    print("\nWelcome to the Memory Agent Chat!")
    print("Your reminders will be remembered across chats.")
    print("Type 'exit' to quit the chat.\n")
    
    while True:
        # Get user input
        user_input = input("User: ")
        
        # Check if the user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the chat. Your reminders will be saved to the database.")
            break
        
        # Process the user input and call the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
        
        
if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main_async())