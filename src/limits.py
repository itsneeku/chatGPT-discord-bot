server_limit_per_day = -1  # -1 means no limit
server_limit_per_message = -1  # -1 means no limit
server_daily_total = 0
user_limit_per_day = 10
user_limit_per_message = 10
user_daily_total = {}  # dict to store daily total for each user


def current_limit_message(user_id):
    return (f"**Spending limits**\n```"
            f"{'Server per Day':<20}{'no limit' if server_limit_per_day < 0 else server_limit_per_day : <8} ({server_daily_total} today)\n"
            f"{'Server per Message':<20}{'no limit' if server_limit_per_message < 0 else server_limit_per_message: <8}\n"
            f"{'User per Day':<20}{'no limit' if user_limit_per_day < 0 else user_limit_per_day:<8} ({get_user_daily_total(user_id)} by you today)\n"
            f"{'User per Message':<20}{'no limit' if user_limit_per_message < 0 else user_limit_per_message:<8}"
            f"```")


def is_over_limit(new_cost=1, user_id=None):
    if user_id:
        user_daily_total = get_user_daily_total(user_id)
        if user_limit_per_message >= 0 and new_cost > user_limit_per_message:
            return True
        if user_limit_per_day >= 0 and user_daily_total + new_cost > user_limit_per_day:
            return True
    if server_limit_per_message >= 0 and new_cost > server_limit_per_message:
        return True
    if server_limit_per_day >= 0 and server_daily_total + new_cost > server_limit_per_day:
        return True

    return False


def get_user_daily_total(user_id):
    return user_daily_total.get(user_id, 0)


def add_to_user_daily_total(user_id, new_cost=1):
    user_daily_total[user_id] = user_daily_total.get(user_id, 0) + new_cost


def format_limits_table(user_id):
    limits = get_user_daily_total(user_id)

    table = "```\n"
    table += f"{'Limit Type':<20} {'Value':<10}\n"
    table += "-" * 30 + "\n"
    for limit_type, limit_value in limits.items():
        table += f"{limit_type:<20} {limit_value:<10}\n"
    table += "```"
    return table


def set_limit(limit_type, value) -> bool:
    if value < -1:
        return False
    if limit_type == "server_per_day":
        global server_limit_per_day
        server_limit_per_day = value
        return True
    elif limit_type == "server_per_message":
        global server_limit_per_message
        server_limit_per_message = value
        return True
    elif limit_type == "user_per_day":
        global user_limit_per_day
        user_limit_per_day = value
        return True
    elif limit_type == "user_per_message":
        global user_limit_per_message
        user_limit_per_message = value
        return True
    return False


def add_to_daily_total(new_cost=1):
    global server_daily_total
    server_daily_total += new_cost


def reset_daily(discordClient, logger):
    global server_daily_total
    server_daily_total = 0
    user_daily_total.clear()
    logger.info("Daily total reset to zero")
    # Reset the conversation history or any other daily reset logic
    discordClient.reset_conversation_history()
    logger.info("Recent conversation cleared.")
