import tiktoken, os

# Costs per million tokens
openai_0125_input_cost = os.getenv("OPENAI_0125_INPUT_COST", 0.5)
openai_0125_output_cost = os.getenv("OPENAI_0125_OUTPUT_COST", 1.5)

# Global variable to track if cost calculation is enabled
COST_ENABLED = False

def toggle_cost():
    """
    Toggles the cost calculation setting.
    """
    global COST_ENABLED
    COST_ENABLED = not COST_ENABLED
    return COST_ENABLED

def calculate_token_cost_input(message):
    if not COST_ENABLED:
        return 0
    token_count = get_token_count(message)
    return token_count * openai_0125_input_cost / 1000000

def calculate_token_cost_output(message):
    if not COST_ENABLED:
        return 0
    token_count = get_token_count(message)
    return token_count * openai_0125_output_cost / 1000000

def get_token_count(input):
    if input is None:
        return 0
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(input))