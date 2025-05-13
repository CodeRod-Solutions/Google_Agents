# Email generator agent
# Rod Morrison - CodeRod Solutions LLC
"""
This script defines an "Email Generator Agent" using the Google ADK.
The agent is designed to generate professional emails based on user input
and context. It utilizes a Pydantic model (`EmailOutput`) to ensure
that the generated email (subject and body) is returned in a structured
JSON format.
"""
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# Define output schema for the email generator
# This Pydantic model specifies the structure of the output expected from the LLM.
# It ensures that the agent's response will contain a 'subject' and a 'body' for the email.
class EmailOutput(BaseModel):
    subject: str = Field(
        description="The subject of the email. Should be concise and descriptive.",
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs and signature.",
    )


# --- Create the Email Generator Agent ---
# Initialize the LlmAgent for email generation.
# This agent uses a specified model (e.g., "gemini-2.0-flash") and is given
# detailed instructions on how to generate emails, including guidelines for
# content, tone, and structure.
# The `output_schema` parameter ensures that the agent's output conforms to the EmailOutput model,
# and `output_key` specifies the key under which the structured output will be found.
root_agent = LlmAgent(
    name="email_generator_agent",
    model="gemini-2.0-flash",
    description="Email generator agent that creates professional emails.",
    instruction="""
        You are an email generation assistant.
        Your task is to generate a professional email based on the provided context and user request.
        
        GUIDELINES:
        - Greet the user and ask for the context of the email.
        - Ask for the recipient's name and email address.
        - Ask for the sender's name and title.
        - Create an appropriate subeject line (concise and relevant).
        - Write a well-structured email body with: 
            - A proper greeting
            - Clear and concise main content
            - A polite closing statement
            - A signature line with the sender's name and title
        - Suggest relevant attachments if applicable.
        - Ensure the email is professional and free of grammatical errors.
        - Ensure the email matches the tone and style of the provided context.
        - Keep the mail concise but complete.
        
        IMPORTANT: Your response must be in JSON format following the schema:
        {
            "subject": "<subject>",
            "body": "<email_body>"
        }
        Do not include any other text or explanations outside of the JSON response.
        """,
    output_schema=EmailOutput,
    output_key="email",
)
