from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_reminder(reminder: str, tool_context: ToolContext):
    """
    Adds a reminder to the user's reminder list
    
    Args:
        reminder (str): The reminder text to be added.
        tool_context: Context for accessing and updating session state
        
    Returns:
        str: Confirmation message indicating the reminder has been added.
    """
    
    print(f"--- Tool: add_reminder called for '{reminder}' ---")
    # Retrieve the current reminders from the session state.
    reminders = tool_context.state.get("reminders", [])
    
    # Append the new reminder to the list.
    reminders.append(reminder)
    
    # Update the session state with the new reminders list.
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }
    
    
def view_reminders(tool_context: ToolContext):
    """
    Args:
        tool_context (ToolContext): Context for accessing session state.
    
    Returns:
        str: A formatted string of all reminders.
    """
    print("--- Tool: view_reminders called ---")
    
    reminders = tool_context.state.get("reminders", [])
    
    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}
        

def update_reminder(index: int, updated_text: str, tool_context: ToolContext):
    """ Update an existing reminder
    Args:
        index (int): The index of the reminder to update.
        updated_text (str): The new text for the reminder.
        tool_context (ToolContext): Context for accessing and updating session state.
    Returns:
        str: Confirmation message indicating the reminder has been updated.
    """
    
    print(
        f"Tool update_reminder called for index {index} with text '{updated_text}' ---"
    )
    
    # Get the current reminders from the session state.
    reminders = tool_context.state.get("reminders", [])
    
    # check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"Could not find reminder at index {index}. Currently there are {len(reminders)} reminders.",
        }
        
    # Update the reminder at the specified index (1-based index).
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text
    
    # Upddate the session state with the modified reminders list.
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"Updated reminder from '{old_reminder}' to '{updated_text}' at index {index}.",
    }
    
def delete_reminder(index: int, tool_context: ToolContext):
    """Delete a reminder at the specified index.
    Args:
        index (int): The index of the reminder to delete.
        tool_context (ToolContext): Context for accessing and updating session state.
        
    Returns:
        str: Confirmation message indicating the reminder has been deleted.
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")
    
    # Get current reminders from the session state.
    reminders = tool_context.state.get("reminders", [])
    
    # Check if the index is valid.
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"Could not find reminder at index {index}. Currently there are {len(reminders)} reminders.",
        }
        
    # Remove the reminder at the specified index (1-based index).
    deleted_reminder = reminders.pop(index - 1)
    
    # Update the session state with the modified reminders list.
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"Deleted reminder '{deleted_reminder}' at index {index}.",
    }
    
def update_user_name(name: str, tool_context: ToolContext):
    """Update the user's name
        Args:
            name (str): The new name to set for the user.
            tool_context (ToolContext): Context for accessing and updating session state.
        
        Returns:
            A confirmation message indicating the user's name has been updated.
        """
    print(f"--- Tool: update_user_name called for '{name}' ---")
    
    # Get the current user name from the session state.
    old_name = tool_context.state.get("user_name", "")
    
    # Update the user name in the session state.
    tool_context.state["user_name"] = name
    
    
    return {
        "action": "update_user_name",
        old_name: old_name,
        "new_name": name,
        "message": f"User name updated to: {name}",
    }
    
# Create the memory agent with the defined tools.
memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A smart reminder agent with persistent memory.",
    instruction="""
    You are a friendly reminder agent the remember users across conversations.
    
    The user's information is stored in state: 
    - User Name: {user_name}
    - Reminders: {reminders}
    
    You can help the users with their reminders with the following capabilities:
    1. Add a reminder
    2. View existing reminders
    3. Update a reminder
    4. Delete a reminder
    5. Update the user's name
    
    Always be friendly and address the user by their name. If you do not know the user's name, ask them to provide it 
    and use the update_user_name tool to set it when they introduce themselves.
    
    **REMINDER MANGEMENT GUIDELINES**
    
      1. When the user asks to update or delete a reminder but doesn't provide an index:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"), 
         look through the reminders to find a match
       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on
    
    4. For viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some
    
    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" → add_reminder("buy milk"))
    
    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which reminder the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)