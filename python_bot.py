import discord
from discord.ext import commands
from utils.config import TOKEN, ADMIN_USERS
from utils.commands import *

print(TOKEN)


def is_admin(user_id):
    return user_id in ADMIN_USERS


intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


@bot.tree.command(name="ping", description="Responds with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)


@bot.tree.command(name="stopserver", description="Stop the server")
async def stopserver(interaction: discord.Interaction):
    try:
        result = send_down()
        if result.returncode == 0:
            return await interaction.response.send_message(f"Server stopped.")
        else:
            return await interaction.response.send_message(f"Error: {result.stderr}")
    except Exception as e:
        return await interaction.response.send_message(f"Exception encountered: {e}")


@bot.tree.command(name="startserver", description="Start server with a save")
async def startserver(interaction: discord.Interaction, sauvegarde: str | None = None):
    saves = get_saves_list()
    chosen_save = sauvegarde
    print(saves)
    print(chosen_save)

    if chosen_save is not None and chosen_save in saves:
        try:
            chosen_save = saves[int(chosen_save)]
        except Exception as e:
            (lambda _: _)(e)
        try:
            resultat = send_start(chosen_save)
        except Exception as e:
            return await interaction.response.send_message(f"Lancement raté: {e}\n")

        if not resultat.returncode:
            return await interaction.response.send_message(f"Serveur lancé avec la sauvegarde {chosen_save}.")
        else:
            return await interaction.response.send_message(f"Lancement raté: {resultat.stderr}")
    else:
        saves_formatted = "\n".join([f"`{i}`: `{s}`" for i, s in enumerate(saves)])
        await interaction.response.send_message(f"Liste des sauvegardes disponibles: \n{saves_formatted}")


@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("Slash commands synced!")


if __name__ == "__main__":
    bot.run(TOKEN)
