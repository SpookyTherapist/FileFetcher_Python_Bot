import discord
from discord.ext import commands
import io

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='find_files')
async def find_files(ctx, search_string):
    files_found = []

    async for message in ctx.channel.history(limit=100):
        for attachment in message.attachments:
            if search_string.lower() in attachment.filename.lower():
                # Download the file
                file_content = await attachment.read()

                # Re-upload the file
                file = discord.File(io.BytesIO(file_content), attachment.filename)
                files_found.append((file, message.id))  # Store both the file and message ID

    if files_found:
        response = "\n".join([f"File found with '{search_string}' in message (ID: {message_id}):" for _, message_id in files_found])
        await ctx.send(response, files=[file for file, _ in files_found])
    else:
        await ctx.send(f"No files found with '{search_string}' in the last 100 messages.")


bot.run('YOUR TOKEN')
