import discord
import time
from discord.ext import commands
from utils.config import DISCORD_BOT_TOKEN, ADMIN_USERS, YES, PICTURES, picture_directory
from utils.commands import *
from utils.tools import download_file
from random import choice, seed

def is_admin(user_id):
    return str(user_id) in ADMIN_USERS


intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


@bot.tree.command(name="ping", description="Répond avec pong.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)


@bot.tree.command(name="stopserver", description="Arrête le serveur.")
async def stopserver(interaction: discord.Interaction):
    try:
        result, _ = send_down()
        if result.returncode == 0:
            return await interaction.response.send_message(f"Serveur arrêté.")
        else:
            return await interaction.response.send_message(f"Erreur: {result.stderr}")
    except Exception as e:
        return await interaction.response.send_message(f"Erreur: {e}")


@bot.tree.command(name="startserver", description="Lance le serveur avec une certaine sauvegarde.")
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
            resultat, _ = send_start(chosen_save)
        except Exception as e:
            return await interaction.response.send_message(f"Lancement raté: {e}\n")

        if not resultat.returncode:
            return await interaction.response.send_message(f"Serveur lancé avec la sauvegarde {chosen_save}.")
        else:
            return await interaction.response.send_message(f"Lancement raté: {resultat.stderr}")
    else:
        saves_formatted = "\n".join([f"`{i}`: `{s}`" for i, s in enumerate(saves)])
        await interaction.response.send_message(f"Liste des sauvegardes disponibles: \n{saves_formatted}")


@bot.tree.command(name="oui", description="Lance-moi.")
async def oui(interaction: discord.Interaction, texte: str = ""):
    return await interaction.response.send_message(f"<@{YES}>{', ' if len(texte) else ''}{texte}")


@bot.tree.command(name="randompicture", description="Affiche une image aléatoire.")
async def randompicture(interaction: discord.Interaction):
    seed(time.time())
    rand_pict = choice(PICTURES)
    return await interaction.response.send_message(file=discord.File(open(rand_pict, 'rb')))


@bot.tree.command(name="uploadpicture", description="Non. Tu t'es trompé.")
async def uploadpicture(interaction: discord.Interaction,
                        media: discord.Attachment,
                        media2: discord.Attachment | None = None,
                        media3: discord.Attachment | None = None,
                        media4: discord.Attachment | None = None,
                        media5: discord.Attachment | None = None,
                        media6: discord.Attachment | None = None,
                        media7: discord.Attachment | None = None,
                        media8: discord.Attachment | None = None,
                        media9: discord.Attachment | None = None,
                        media10: discord.Attachment | None = None):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("Non, tu t'es encore trompé.")
    attachments = []

    def add_valid_pictures(attachment):
        if attachment and attachment.content_type and (attachment.content_type.startswith("image/")
                                                       or attachment.content_type.startswith("video/")):
            attachments.append(attachment)

    add_valid_pictures(media)
    add_valid_pictures(media2)
    add_valid_pictures(media3)
    add_valid_pictures(media4)
    add_valid_pictures(media5)
    add_valid_pictures(media6)
    add_valid_pictures(media7)
    add_valid_pictures(media8)
    add_valid_pictures(media9)
    add_valid_pictures(media10)
    if not len(attachments):
        return await interaction.response.send_message("Pas de média valide.", ephemeral=True)
    saved_paths = []
    for file in attachments:
        saved_paths.append(download_file(file.url, picture_directory, "pic"))
    PICTURES.extend(saved_paths)  #  Otherwise, the uploaded pictures would only be available on next bot reboot.
    joint = "\n"
    return await interaction.response.send_message(f"Enregistré sous\n{joint.join(saved_paths)}", ephemeral=True)


@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("Slash commands synced!")


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
