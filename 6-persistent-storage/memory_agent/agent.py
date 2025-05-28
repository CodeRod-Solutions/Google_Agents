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
    