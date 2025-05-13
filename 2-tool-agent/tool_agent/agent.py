"""
This script defines a "Tool Agent" using the Google ADK.
The agent is configured to use Google Search as a tool.
It demonstrates how to integrate tools into an agent's capabilities.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

# Example of a custom tool function to get the current time.
# This function is currently commented out but can be enabled
# by uncommenting it and adding it to the agent's tools list.
# from datetime import datetime # Required if get_current_time is used
# def get_current_time() -> dict:
#     """
#     Get the current time in the format YYYY-MM-DD HH:MM:SS
#     """
#     return {
#         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

# Define the root agent for the tool application.
# This agent is configured with a name, the model to use (e.g., "gemini-2.0-flash"),
# a description, and instructions on its behavior and available tools.
# Currently, it's set up to use the `google_search` tool.
root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search],
    # Example of how to add the custom get_current_time tool:
    # tools=[get_current_time],
    # Example of how to add multiple tools (Note: ensure compatibility and correct implementation):
    # tools=[google_search, get_current_time], # <--- Original comment notes this doesn't work, may require specific ADK handling for multiple tools.
)
