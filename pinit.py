#! /usr/bin/env python3
"""
A python script for running the pinit Discord bot.
"""
import discord

__version__ = '1.0'

client = discord.Client()
emoji = '📌'


class error():
    """
    Error strings.
    """
    Forbidden = "I do not have permissions to %spin the message."
    NotFound = "The message or channel was not found or deleted."
    HTTPException = "%sinning the message failed%s."


async def handle_message(payload):
    """
    Returns reaction message. Returns None instead if payload is irrelevant.
    """
    if str(payload.emoji) != emoji:
        return None

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.type != discord.MessageType.default:
        return None

    return message


async def stderr(user_id, message, content):
    """
    Error output.
    """
    user = client.get_user(user_id)

    try:
        await message.channel.send("%s %s" % (content, user.mention))

    except (discord.HTTPException, discord.Forbidden):
        await user.send(content)


@client.event
async def on_raw_reaction_add(payload):
    message = await handle_message(payload)

    if message is None or message.pinned:
        return

    try:
        await message.pin()
        return

    except discord.Forbidden:
        content = error.Forbidden % ("")

    except discord.NotFound:
        content = error.NotFound

    except discord.HTTPException:
        content = error.HTTPException % (
            "P", ", probably due to the channel having more than 50 pinned "
            "messages")

    # Exception handling
    await stderr(payload.user_id, message, content)


@client.event
async def on_raw_reaction_remove(payload):
    message = await handle_message(payload)

    if message is None or not message.pinned:
        return

    try:
        await message.unpin()
        return

    except discord.Forbidden:
        content = error.Forbidden % ("un")

    except discord.NotFound:
        content = error.NotFound

    except discord.HTTPException:
        content = error.HTTPException % ("Unp", "")

    # Exception handling
    await stderr(payload.user_id, message, content)


def main():
    client.run('xxx')


if __name__ == '__main__':
    main()
