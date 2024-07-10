limit_per_day = -1  # -1 means no limit
limit_per_message = -1  # -1 means no limit
daily_total = 0


def current_limit_message():
    return f"**Spending limits**\n Per Day           : {'unlimited' if limit_per_day < 0 else limit_per_day}  ({daily_total} spent today)\n Per Message : {'unlimited' if limit_per_message < 0 else limit_per_message}"


def is_over_limit(new_cost=1):
    if limit_per_message >= 0 and new_cost > limit_per_message:
        return True
    if limit_per_day >= 0 and daily_total + new_cost > limit_per_day:
        return True
    return False


def set_limit(limit_type, value) -> bool:
    if value < -1:
        return False
    if limit_type == "per_day":
        global limit_per_day
        limit_per_day = value
        return True
    elif limit_type == "per_message":
        global limit_per_message
        limit_per_message = value
        return True
    return False


def add_to_daily_total(new_cost=1):
    global daily_total
    daily_total += new_cost


def reset_daily(discordClient, logger):
    global daily_total
    daily_total = 0
    logger.info("Daily total reset to zero")
    # Reset the conversation history or any other daily reset logic
    discordClient.reset_conversation_history()
    logger.info("Recent conversation cleared.")
