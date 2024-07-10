# Global variable to track if cost calculation is enabled
COST_ENABLED = False

def toggle_cost():
    """
    Toggles the cost calculation setting.
    """
    global COST_ENABLED
    COST_ENABLED = not COST_ENABLED
    return COST_ENABLED

def calculate_token_cost(message):
    if not COST_ENABLED:
        return 0
    cost = len(message)
    return cost