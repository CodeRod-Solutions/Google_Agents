from google.adk.agents import Agent

# Create the root agent

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