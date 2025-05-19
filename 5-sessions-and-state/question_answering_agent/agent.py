"""
This script defines a "Question Answering Agent" using the Google ADK.
The agent is designed to answer user questions by leveraging information
stored in the session state, specifically the user's name and preferences.
The instruction prompt includes placeholders (`{user_name}` and `{user_preferences}`)
that are intended to be populated from the active session's state during runtime.
"""

from google.adk.agents import Agent

# Create the root agent for question answering.
# This agent is configured with a name, the model to use (e.g., "gemini-2.0-flash"),
# a description, and a detailed instruction prompt.
# The instruction prompt is crucial as it guides the LLM's behavior and
# utilizes placeholders `{user_name}` and `{user_preferences}`. These placeholders
# are expected to be dynamically filled by the ADK runtime using values
# from the current session's state, allowing the agent to personalize its responses.
question_answering_agent = Agent(
    name="question_answering_agent",
    model="gemini-2.0-flash",
    description="Question anwering agent",
    instruction="""
    You are a helpful assistant that answers questions based on the user's preferences.
    
    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
)
