import openai
import discord
from discord import app_commands
import os
from dotenv import load_dotenv


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"The bot has logged in as {self.user}.")


client = Client()
tree = app_commands.CommandTree(client)
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


@tree.command(name="start", description="Start a chat with AI.")
async def start(interaction: discord.Interaction, prompt: str):


    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Respond to: {prompt}",
    )
    await interaction.response.send_message(response["choices"][0]["text"])

client.run(os.getenv("BOT_TOKEN"))