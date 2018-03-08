# Code taken from JellyWX's reminder-bot for Discord.
# https://github.com/JellyWX/reminder-bot/blob/master/format_time.py
# Donate to him at https://www.patreon.com/jellywx and add his bot with
# https://discordapp.com/oauth2/authorize?client_id=349920059549941761&scope=bot&permissions=268446820


import time

def format_time(text):
    current_buffer = '0'
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    for char in text:
        if char == 's':
          seconds = int(current_buffer)
          current_buffer = '0'

        elif char == 'm':
          minutes = int(current_buffer)
          current_buffer = '0'

        elif char == 'h':
          hours = int(current_buffer)
          current_buffer = '0'

        elif char == 'd':
          days = int(current_buffer)
          current_buffer = '0'

        else:
          try:
            int(char)
            current_buffer += char
          except ValueError:
            return None

    time_sec = round(seconds + (minutes * 60) + (hours * 3600) + (days * 86400) + int(current_buffer))
    return time_sec
