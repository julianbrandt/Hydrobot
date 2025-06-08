from typing import Union
import discord
import os
from dotenv import load_dotenv

load_dotenv()

from MemePy import MemeGenerator

from meme_templates import MEME_TEMPLATES

intents = discord.Intents.default()
intents.message_content = True

# hydrobot = Hydrobot(intents=intents)
hydrobot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(hydrobot)

for template in MEME_TEMPLATES:
    required_args_count = len([a for a in template.text_areas if a])
    optional_args_count = len([a for a in template.text_areas if not a])
    required_args = [[f"text_{i}", "str"] for i in range(1, required_args_count + 1)]
    optional_args = [[f"text_{i}", "Union[str, None]"] for i in range (required_args_count + 1, required_args_count + optional_args_count + 1)]
    stretch_arg = [["image_stretch", "Union[bool, None]"]]
    args = required_args + optional_args + stretch_arg
    args_str = ", ".join(map(": ".join, args))
    function_name = f"meme_{template.id}"
    function_description = f"Generate '{template.name}' meme"

    function_string = f"""
@tree.command(name="{function_name}", description="{function_description}")
async def {function_name}(interaction: discord.Interaction, {args_str}):
    await interaction.response.defer(thinking=True)
    try:
        texts = [{", ".join(map(lambda x: x[0], required_args))}]
        {
            "; ".join(map(lambda arg: f"texts += [{arg[0]}] if {arg[0]} is not None else []", optional_args))
        }
        if {stretch_arg[0][0]}:
            texts += ['{{stretch}}']
        await interaction.followup.send(file=discord.File(MemeGenerator.get_meme_image_bytes('{template.id}', texts), filename='{template.filename}'))
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {{e}}")
"""
    exec(function_string, globals(), locals())

@hydrobot.event
async def on_ready():
    await tree.sync()

hydrobot.run(os.getenv('HYDROBOT_TOKEN') or "missing token")

