# Dad Joke Agent using LiteLLM
"""
This script defines a "Dad Joke Agent" using the Google ADK and LiteLLM.
The agent is designed to tell dad jokes when invoked. It uses a predefined list
of jokes and can be extended to fetch jokes from an external API or use a more
sophisticated joke generation model.
"""

import os
import random
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Initialize the LiteLlm model configuration.
# This specifies the underlying LLM to be used (e.g., OpenAI's gpt-4o)
# and the necessary API key for authentication.
model = LiteLlm(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def get_dad_joke():
    """
    Selects and returns a random dad joke from a predefined list.

    Returns:
        str: A randomly selected dad joke.
    """
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I used to play piano by ear, but now I use my hands.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
    ]
    return random.choice(jokes)


# Define the root agent for the dad joke application.
# This agent is configured with a name, the LiteLlm model, a description,
# and specific instructions on how to behave. It is also equipped with
# the `get_dad_joke` tool to provide jokes.
root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="A dad joke agent that tells dad jokes.",
    instruction="""
        You are a helpful assistant that tells dad jokes.   \
        Only use the the tool: `dad_joke_agent` to tell jokes".
        """,
    tools=[get_dad_joke],
)
