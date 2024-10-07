@client.event
async def on_ready():
    print(f'bot connected as {client.user.name}')
    await client.change_presence(activity=discord.Game(name="ILL FUCKING SLAUGHTER YOU BITCH YOU FUCKING LOSER COME DIE TO ME LOL"))

async def update_channel_name(channel):
    global toggle_groupchat, groupchat_name, number

    while toggle_groupchat:
        await channel.edit(name=f'{groupchat_name} {number}')
        number += 1
        if not toggle_groupchat:
            break
        await asyncio.sleep(0.0010101000000000000000000001010010010100101010101010010101010101000000010010010101010010010010100100101001010100101010100101010101001010010100101001001001010010100010)
        
@client.event
async def on_message(message):
    global toggle_groupchat, groupchat_name, number
    global responding, send, target_user, respond, send_messages, message_option_2, keep_going, sending_speed, is_rated, sentences, reacting, custom_emoji
    global mocking, mimicing_self, stop_cooldown, mimicking, responding, activity_name, mock, ar, current_sentence, respond, sentences_replying, autoreplying, sniped_messages, afk_mode, afk_response
        
    # HELP 
    if message.content.lower() == 'help' and message.author.id == 1250429319239565375:
        await message.delete()
###########################
