from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from rich import print


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """Get a nerd joke based on the topic."""
    print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

    # Example jokeds, in a real scenario this could be an API call or a database query
    jokes = {
        "python": "Why don't Python programmers like to use inheritance? Because they don't like to inherit anything!",
        "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache!",
        "java": "Why do Java developers wear glasses? Because they can't C#!",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "math": "Why was the equal sign so humble? Because he knew he wasn't less than or greater than anyone else!",
        "physics": "Why did the photon check a hotel? Because it was travelling light!",
        "chemistry": "Why did the acid go to the gym? To become a buffer solution!",
        "biology": "Why did the cell go to therapy? Because it had too many issues!",
        "default": "Why did the computer go to the doctor? Because it had a virus!",
    }

    joke = jokes.get(topic.lower(), jokes["default"])

    # Update the state with the last joke
    tool_context.state["last_joke_topic"] = topic

    return {"status": "success", "joke": joke, "topic": topic}


# Create the funny nerd agent
funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-2.0-flash",
    description="An agent that tells nerd jokes based on a given topic.",
    instruction="""
    You are a funny nerd agent that tells nerdy jokes about various topics.
    
    When asked to tell a joke:
    1. Use the get_nerd_joke tool to fetch a joke about the requested topic
    2. If no specific topic is mentioned, ask the user what kind of nerdy joke they'd like to hear
    3. Format the response to include both the joke and a brief explanation if needed
    
    Available topics include:
    - python
    - javascript
    - java
    - programming
    - math
    - physics
    - chemistry
    - biology
    
    Example response format:
    "Here's a nerdy joke about <TOPIC>:
    <JOKE>
    
    Explanation: {brief explanation if needed}"

    If the user asks about anything else, 
    you should delegate the task to the manager agent.
    """,
    tools=[get_nerd_joke],
)
