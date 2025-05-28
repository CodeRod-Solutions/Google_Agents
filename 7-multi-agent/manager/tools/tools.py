from datetime import datetime

def get_current_time() -> dict:
    """
    Returns the current time YYYY-MM-DD HH:MM:SS.
    
    Returns:
        str: Current time as a string in YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
    }