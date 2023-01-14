import openai
import discord
from discord import app_commands
import os
from dotenv import load_dotenv


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"The bot has logged in as {self.user}.")


def check_is_running(discord_id):
    try:
        running = user_settings[discord_id]["running"]
        return running
    except:
        return False


client = Client()
tree = app_commands.CommandTree(client)
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
user_settings = {}


@tree.command(name="start", description="Start a chat with AI.")
async def start(interaction: discord.Interaction):
    await interaction.response.defer()

    running = check_is_running(interaction.user.id)
    if running:
        await interaction.followup.send("You are already in a chat.")
        return

    try:
        user_settings[interaction.user.id]["running"] = True
    except:
        user_settings[interaction.user.id] = {"running": True}

    await interaction.followup.send("Started a chat with MaxiGPT. Just send the message and I will respond!")


@tree.command(name="stop", description="Stop the chat with AI.")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()

    running = check_is_running(interaction.user.id)
    if not running:
        await interaction.followup.send("You are not in a chat.")
        return

    user_settings[interaction.user.id]["running"] = False

    await interaction.followup.send("Stopped the chat with MaxiGPT.")


@client.event
async def on_message(message: discord.Message):
    running = check_is_running(message.author.id)
    if running:
        async with message.channel.typing():
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"User: {message.content} AI: ",
                max_tokens=4000
            )

            await message.channel.send(response["choices"][0]["text"])


client.run(os.getenv("BOT_TOKEN"))