# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random

import os
token = os.environ['DISCORD_TOKEN']
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def question(ctx, question_link: str):
    # Check if the command is used in the #general channel
    if ctx.channel.name == 'general':
        # Notify everyone in the #questions channel
        channel = discord.utils.get(ctx.guild.channels, name='question')
        if channel:
            await channel.send(f'New question from {ctx.author.mention}!')
            await channel.send(question_link)
        else:
            await ctx.send('Error: #question channel not found.')
    else:
        await ctx.send('Error: Please use the ?question command in the #general channel.')

@bot.command()
async def submit(ctx):
    # Check if the command is used in the correct channel
    if ctx.channel.name == 'general':
        # Check if an image is attached
        if ctx.message.attachments:
            # Get the submission channel
            submission_channel = discord.utils.get(ctx.guild.channels, name='submission')
            if submission_channel:
                # Mention the user who submitted
                submission_message = f'{ctx.author.mention} has submitted an image!'

                # Choose a random cheerful response
                cheerful_responses = [
                    'Great job!',
                    'Fantastic!',
                    'Awesome work!',
                    'You nailed it!',
                    'Keep up the good work!'
                ]
                random_response = random.choice(cheerful_responses)

                # Send the submission message and the random response
                await submission_channel.send(submission_message)
                await submission_channel.send(random_response)

                await ctx.send('Submission successful!')
            else:
                await ctx.send('Error: #submission channel not found.')
        else:
            await ctx.send('Please provide an image with your submission.')
    else:
        await ctx.send('Error: Please use the ?submit command in the #general channel.')




bot.run(token)