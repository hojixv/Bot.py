import discord
import requests
import asyncio
import os
import random
import time
import pyfiglet  # Import pyfiglet for ASCII art

# Print the custom ASCII art when the script starts
ascii_art = r"""
print(ascii_art)

# Initialize client
client = discord.Client(intents=discord.Intents.default(), self_bot=True)

# Default variables for AFK check
afk_check_running = False

# Default reaction emojis
reaction_emoji_set = '☠'
pause_reaction_script_set = False
reaction_emoji_rt = '🤡'
reaction_emoji_nerd = '🤓'

# Target user IDs for RT, nerd, and monitoring
target_user_id_rt = None
target_user_id_monitor = None
target_user_id_reaction = None

# Default user IDs for controlling the commands
command_controller_id = 1219015881988898978
control_user_id = 1219015881988898978

# Default variables for controlling group chat name changes
channel_id = None
count = 1
last_action_time = 0
rate_limit_reset_time = 0
running = False

# Initializing target_users for 
target_users = {}
spamming = False
spam_messages = []
token_user_id = None
paused = False

# Function to send messages with rate limit handling
async def send_message_with_retry(channel, message):
    while True:
        try:
            await channel.send(message)
            return  # Message sent successfully
        except discord.errors.HTTPException as e:
            if e.status == 429:  # Rate limit hit
                print(f"Rate limit hit. Retrying after 3.5 seconds.")
                await asyncio.sleep(3.5)  # Wait for rate limit reset plus 3.5 seconds
            else:
                print(f"An error occurred while sending message: {e}")
                return  # Failed to send message

# Function to get user ID from the token
def get_user_id(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("Failed to retrieve user ID. Check your token.")
        exit()

# Prompt for the user's token for both functionalities
user_token = input(" Enter Your Token: ")

# Get user ID for authorization
authorized_user_id = int(get_user_id(user_token))

# Client event for when the bot is ready
@client.event
async def on_ready():
    global token_user_id
    print(f'Logged in as {client.user}')
    token_user_id = authorized_user_id

# Event listener for handling messages
@client.event
async def on_message(message):
    global afk_check_running, reaction_emoji_set, pause_reaction_script_set
    global reaction_emoji_rt, target_user_id_rt, channel_id, count
    global last_action_time, rate_limit_reset_time, running
    global target_users, spamming, spam_messages, paused
    global target_user_id_monitor, target_user_id_reaction

    # AFK check command handling
    if message.author.id == authorized_user_id:
        if message.content.startswith('!afkcheck') and not afk_check_running:
            target_id = message.content.split()[1]
            try:
                target = await client.fetch_user(int(target_id))
            except discord.errors.NotFound:
                await message.channel.send(f"User with ID {target_id} not found.")
                return
            
            afk_check_running = True

            # Send countdown message from 100 to 0 with a delay between each message
            for i in range(100, -1, -1):
                if not afk_check_running:
                    break
                await asyncio.sleep(1)  # Add a delay of 1 seconds
                await send_message_with_retry(message.channel, f"{i} <@{target_id}>")
            
            if afk_check_running:
                # Ping the target user
                await send_message_with_retry(message.channel, f"{target.mention} shitcan folded to its lord LOL.")
            afk_check_running = False
        
        elif message.content.startswith('!stopafk') and afk_check_running:
            afk_check_running = False
            await message.channel.send("AFK check stopped.")

    # Set command handling
    if message.author.id == authorized_user_id:
        if message.content.startswith('!stopset'):
            # Pausing the reaction script for Set command
            pause_reaction_script_set = True
            await message.channel.send("Pausing the reaction script for Set command.")
        elif message.content.startswith('!resume'):
            # Resuming the reaction script for Set command
            pause_reaction_script_set = False
            await message.channel.send("Resuming the reaction script for Set command.")
        elif message.content.startswith('!set'):
            # Extracting emoji from message content and changing reaction emoji for Set command
            if not pause_reaction_script_set:
                try:
                    new_emoji = message.content.split(' ')[1]
                    reaction_emoji_set = new_emoji
                    await message.channel.send(f"Reaction emoji set to: {reaction_emoji_set}")
                except IndexError:
                    await message.channel.send("Please provide a valid emoji for Set command.")
            else:
                await message.channel.send("Cannot set reaction emoji while script is paused for Set command.")
    
    # RT command handling
    if message.author.id == authorized_user_id:
        if message.content.startswith('!rt'):
            # Extracting user ID and emoji from message content for RT command
            try:
                command_parts = message.content.split(' ')
                user_id_str = command_parts[1]
                emoji = command_parts[2]
                target_user_id_rt = int(user_id_str)
                reaction_emoji_rt = emoji
                await message.channel.send(f"Reacting to user with ID: {target_user_id_rt} using emoji {reaction_emoji_rt}")
            except (IndexError, ValueError):
                await message.channel.send("Invalid command format. Use '!rt [user_id] [emoji]' to start reacting.")
        elif message.content.startswith('!stoprt'):
            target_user_id_rt = None
            await message.channel.send("Reaction mode stopped for RT command.")
        elif message.content.startswith('!changert'):
            # Extracting emoji from message content for RT command
            try:
                new_emoji = message.content.split(' ')[1]
                reaction_emoji_rt = new_emoji
                await message.channel.send(f"Reaction emoji changed to: {reaction_emoji_rt}")
            except IndexError:
                await message.channel.send("Invalid command format. Use '!changert [emoji]' to change the emoji for RT command.")

    # Reaction handling for Set command
    if message.author.id == authorized_user_id and not pause_reaction_script_set:
        if reaction_emoji_set:
            await message.add_reaction(reaction_emoji_set)
    
    # Reaction handling for RT command
    if message.author.id == target_user_id_rt:
        await message.add_reaction(reaction_emoji_rt)
        
    # !black command handling
    if message.author.id == authorized_user_id:
        if message.content.startswith('!black'):
            try:
                user_id = int(message.content.split()[1].strip('<@!>'))
                percentage = random.randint(1, 100)
                await message.channel.send(f"<@{user_id}> is {percentage}% black‍.")
            except (IndexError, ValueError):
                await message.channel.send("Please provide a valid user ID. Usage: `!black <userid>`")
                
    # Control command for changing group chat name
    if message.author.id == control_user_id:
        if message.content == "!gcc":
            channel_id = message.channel.id
            running = True
            count = 1  # Set count to 1 when GCC starts
            client.loop.create_task(spam_change_name())
        elif message.content == "!stopgcc":
            running = False
            count = 1  # Reset count to 1 when GCC is stopped

    # Rpc command handling
    if message.author.id == authorized_user_id:
        if message.content.startswith('!rpc '):
            name = message.content[5:].strip('"')
            await client.change_presence(activity=discord.Streaming(name=name, url="https://twitch.tv/ex"))
            await message.channel.send(f'Rich Presence name set to "{name}"!')

    # SMG command handling
    if message.author.id == token_user_id:
        # Check if the message is the "!smg" command followed by a user mention
        if message.content.startswith("!blaze "):
            try:
                parts = message.content.split(" ", 1)
                user_mention = parts[1].strip()
                # Extracting user ID from mention
                target_users[message.channel.id] = user_mention
                await message.channel.send(f"Reacting to user: {user_mention} in channel {message.channel.id}")  # Send a message in the channel
                if spamming:
                    await send_spam_messages(message.channel)
            except (IndexError, ValueError):
                await message.channel.send("Invalid command format. Use: !blaze <@user_mention>")
        
        # Check for start spamming command
        if message.content.startswith("!blaze"):
            spamming = True
            channel_id = message.channel.id
            if channel_id in target_users:
                try:
                    # Search for smg.txt in the Documents directory
                    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
                    smg_file_path = os.path.join(documents_path, 'smg.txt')
                    with open(smg_file_path, 'r') as file:
                        spam_messages = file.readlines()
                        await send_spam_messages(message.channel)
                except FileNotFoundError:
                    print("smg.txt not found in Documents directory. Make sure the file exists in the Documents folder.")
            else:
                await message.channel.send("Please specify a target user mention using !smg <@user_mention> in the desired channel before starting the spamming.")
        
        # Check for stop spamming command
        if message.content == "!stopblaze":
            paused = True
            spamming = False
            await message.channel.send("Script paused.")

        # Check for resume command
        if message.content == "!resumeblaze":
            paused = False
            await message.channel.send("Script resumed.")
        
        # Check for cmds command
        if message.content == "!cmds":
            commands_list = [
                 "```─────────────────────────────────────────────────────────────────────────────────────────────────────",
                "[ = ] - !stopset - Pause the reaction script for Set command.",
                "[ = ] - !resume - Resume the reaction script for Set command.",
                "[ = ] - !set [emoji] - Set reaction emoji for Set command.",
                "[ = ] - !rt [user_id] [emoji] - React to user with specified emoji for RT command.",
                "[ = ] - !stoprt - Stop reacting to user for RT command.",
                "[ = ] - !changert [emoji] - Change reaction emoji for RT command.",
                 "─────────────────────────────────────────────────────────────────────────────────────────────────────",
                "[ = ] - !gcc - Start changing group chat names.",
                "[ = ] - !stopgcc - Stop changing group chat names.",
                "[ = ] - !rpc [status] - Change your Rich Presence status.",
                "[ = ] - !blaze [@user_mention] - Start reacting to a user with spam messages.",
                "[ = ] - !stopblaze - Pause spamming messages.",
                "[ = ] - !resumeblaze - Resume spamming messages.",
                "[ = ] - !afkcheck [userid] - Initiates an AFK check",
                "[ = ] - !stopafk - Stops the ongoing AFK check.",
                 "─────────────────────────────────────────────────────────────────────────────────────────────────────",
                "[ = ] - !nerd [userid] - Quotes the user's message and reacts to it with a 🤓 emoji.",
                "[ = ] - !stopnerd - Stop's quoting the user.",
                 "─────────────────────────────────────────────────────────────────────────────────────────────────────```",
            ]
            # Send the commands list
            cmd_msg = await message.channel.send("```ini\n[Valhala's Selfbot:]```\n" + "\n".join(commands_list))
            # Delete the original command message instantly
            await message.delete()
            # Delete the command message after 2 seconds
            await asyncio.sleep(10)
            await cmd_msg.delete()

    # Nerd monitoring command handling
    if message.author.id == command_controller_id:
        if message.content.startswith('!nerd'):
            try:
                target_user_id_monitor = int(message.content.split(' ')[1])
                target_user_id_reaction = target_user_id_monitor  # Set the reaction target user ID as well
                await message.channel.send(f"{target_user_id_monitor} is a nerd 🤓")
            except (ValueError, IndexError):
                await message.channel.send("Invalid user ID.")
        elif message.content.startswith('!stopnerd'):
            # Stop monitoring and reaction
            target_user_id_monitor = None
            target_user_id_reaction = None
            await message.channel.send("woah he isnt a nerd anymore")

    # Check if the message is from the target user ID for monitoring
    if target_user_id_monitor is not None and message.author.id == target_user_id_monitor:
        # Send the message with the 🤓 reaction
        await message.channel.send(f'"{message.content}" 🤓')

    # Check if the message is from the target user ID for reaction
    if target_user_id_reaction is not None and message.author.id == target_user_id_reaction:
        # React with 🤓
        await message.add_reaction(reaction_emoji_nerd)

# Function to change the group chat name
async def change_groupchat_name(groupchat, count):
    global rate_limit_reset_time
    try:
        await groupchat.edit(name=f"YOUR ASS WTF DORK ASS NIGGA {count}")
        print(f"changed the gc name {count}")
    except discord.Forbidden:
        print(f"Changing the name of group chat {groupchat.name} failed due to permissions.")
    except discord.HTTPException as e:
        if e.status == 429:  # Handle rate limiting
            retry_after = e.retry_after
            print(f"Rate limit hit. Retrying after {retry_after} seconds.")
            rate_limit_reset_time = time.time() + retry_after
            await asyncio.sleep(retry_after)
        else:
            print(f"An error occurred while changing the name of group chat {groupchat.name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to control spamming name changes
async def spam_change_name():
    global count
    global last_action_time
    global rate_limit_reset_time
    global running
    while count <= 30000 and running:
        current_time = asyncio.get_event_loop().time()
        elapsed_time = current_time - last_action_time
        if current_time >= rate_limit_reset_time and elapsed_time >= 0.1:  # If more than 0.1 seconds have passed since last action
            last_action_time = current_time
            if channel_id:
                groupchat = client.get_channel(channel_id)
                if groupchat and isinstance(groupchat, discord.GroupChannel):
                    await change_groupchat_name(groupchat, count)
                    count += 1
                    if count % 100 == 0:  # Add a 2-second cooldown every 100 changes
                        await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.1)  # Adjusting the delay to avoid high CPU usage

# Function to send spam messages
async def send_spam_messages(channel):
    global spamming, paused
    while spamming and not paused:
        for message in spam_messages:
            formatted_message = f"{message.strip()} {target_users[channel.id]}"
            await asyncio.sleep(0.4)  # Adding a delay of 0.4 seconds before sending each message
            if not paused:
                await send_with_rate_limit(channel, formatted_message)

# Function to send message with rate limit handling
async def send_with_rate_limit(channel, message):
    global spamming, spam_messages
    # Attempt to send the message
    try:
        await channel.send(message)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            # Write the message to rate.txt
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            rate_file_path = os.path.join(documents_path, 'rate.txt')
            with open(rate_file_path, 'a') as file:
                file.write(f"{message}\n")  # Append the message to rate.txt
        else:
            # Send the entire content of rate.txt
            await send_rate_message(channel)

# Function to send the content of rate.txt
async def send_rate_message(channel):
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    rate_file_path = os.path.join(documents_path, 'rate.txt')
    try:
        with open(rate_file_path, 'r') as file:
            rate_message = file.read()
            await channel.send(rate_message.strip())
    except FileNotFoundError:
        print("rate.txt not found in Documents directory. Make sure the file exists in the Documents folder.")

# Run the client
client.run(user_token, bot=False)
