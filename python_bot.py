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
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="stopserver", description="Stop the server")
async def stopserver(interaction: discord.Interaction):
    await send_message("/stop")
    # TODO: Properly check if server actually stopped.
    await interaction.response.send_message("Server stopped.")


@bot.tree.command(name="startserver", description="Start server with a save")
async def startserver(interaction: discord.Interaction, sauvegarde: str):
    saves = await get_saves()
    # saves = ["oh", "tuot"]  # Alternative hardcoded list
    chosen_save = sauvegarde
    print(saves)
    print(chosen_save)

    if chosen_save in saves:
        reply = await send_message(f"/start {chosen_save}")
        # TODO: Check if successfully started server.
        await interaction.response.send_message(
            f"Serveur lancé avec la sauvegarde {chosen_save}.")
    else:
        saves_formatted = ", ".join([f"`{s}`" for s in saves])
        await interaction.response.send_message(
            f"Liste des sauvegardes disponibles: {saves_formatted}")


@bot.tree.command(name="down", description="Send down command")
async def down(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message(
            "Et non, cette commande n'est pas pour toi.", ephemeral=True)
        return

    await send_message("/down")
    await interaction.response.send_message("Commande `/down` envoyée.",
                                            ephemeral=True)


@bot.tree.command(name="hello", description="Send hello command")
async def hello(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message(
            "Et non, cette commande n'est pas pour toi.", ephemeral=True)
        return

    await send_message("/hello")
    await interaction.response.send_message("Commande `/hello` envoyée.",
                                            ephemeral=True)


@bot.tree.command(name="stop_cmd", description="Send stop_cmd command")
async def stop_cmd(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message(
            "Et non, cette commande n'est pas pour toi.", ephemeral=True)
        return

    await send_message("/stop_cmd")
    await interaction.response.send_message("Commande `/stop_cmd` envoyée.",
                                            ephemeral=True)


# Sync slash commands (you'll need to run this once)
@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("Slash commands synced!")


if __name__ == "__main__":
    bot.run(TOKEN)
