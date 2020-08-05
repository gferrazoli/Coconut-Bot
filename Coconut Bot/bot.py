from discord import *
from connection import *
from random import randint
import time
import dotenv
import os

connection, cursor = connect_to_database()
dotenv.load_dotenv('config.env')
token = os.getenv('token')
client = Client()
users_timestamp = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    game = Game("==help")
    await client.change_presence(status=Status.idle, activity=game)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('==my time spent'):
        try:
            caller_id, voice_id, total_time = select_DiscordUserVoiceSession_from_command_caller(message.author.id, cursor)
            my_time_spent_message = f"Name: <@{caller_id}>\n" \
                                    f"Voice channel name: {client.get_channel(voice_id).name}\n" \
                                    f"Total time spent: {str(int(total_time / 120))} hours"
            await message.channel.send(my_time_spent_message)
        except:
            await message.channel.send("An error has ocurred, please try again later.")

@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    has_joined = before.channel is None and after.channel is not None
    has_left = before.channel is not None and after.channel is None
    has_changed_voice_channel = before.channel is not None and after.channel is not None

    if has_joined:
        set_user_joined_timestamp(member.id)

    if has_left:
        set_user_left_timestamp(member.id, before.channel.id)

    if has_changed_voice_channel:
        set_user_left_timestamp(member.id, before.channel.id)
        set_user_joined_timestamp(member.id)

def set_user_joined_timestamp(member_id: int):
    if select_DiscordUser_from_database(member_id, cursor) is not None:
        users_timestamp[member_id] = time.time()
    else:
        insert_DiscordUser_into_databse(member_id, cursor, connection)
        users_timestamp[member_id] = time.time()

def set_user_left_timestamp(member_id: int, channel_id: int):
    if member_id in users_timestamp:
        joined_timestamp = users_timestamp[member_id]
        left_timestamp = time.time()
        session_amount = left_timestamp - joined_timestamp
        insert_DiscordUserVoiceSession_into_database(member_id, channel_id, session_amount, cursor, connection)
        del users_timestamp[member_id]

client.run(token)
