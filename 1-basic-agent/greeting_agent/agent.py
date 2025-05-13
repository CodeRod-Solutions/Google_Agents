"""
This script defines a "Greeting Agent" using the Google ADK.
The agent is designed to greet the user, ask for their name,
and then greet them by name. It serves as a basic example of
an agent's conversational capabilities.
"""

from google.adk.agents import Agent

# Define the root agent for the greeting application.
# This agent is configured with a name, the model to use (e.g., "gemini-2.0-flash"),
# a description, and specific instructions on how to interact with the user.
root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Greeting agent that greets the user.",
    instruction="""
    You are a helpful assistant that greets the user.
    Ask for the user's name and greet them by name
    """,
)
