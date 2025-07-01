from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
import os
from dotenv import load_dotenv
import subprocess

from utils.commands import *

load_dotenv(".telegram-env")

TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMINS")


async def hello(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def list(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    ls = get_saves_list()
    await update.message.reply_text(f'the list of saves is {ls}')


async def start(update, context):
    try:
        ls = get_saves_list()
        saves = "\n".join([f"{i}: {name}" for i, name in enumerate(ls)])
        mess = "Which save do you want to start?\n" + saves

        # If command has argument (e.g. /start 0 or /start save_name)
        if context.args:
            arg = context.args[0]
            if arg.isdigit() and 0 <= int(arg) < len(ls):
                save_name = ls[int(arg)]
            elif arg in ls:
                save_name = arg
            else:
                await update.message.reply_text("Invalid argument. Please try again.")
                return

        # If this is a reply with a number
        elif update.message.text.isdigit():
            saves_number = int(update.message.text)
            if 0 <= saves_number < len(ls):
                save_name = ls[saves_number]
            else:
                await update.message.reply_text("Invalid number. Please try again.")
                return
        else:
            await update.message.reply_text(mess)
            return

        result, cmd = send_start(save_name)
        if result.returncode == 0:
            await update.message.reply_text(f"Started:\n{cmd}\nOutput:\n{result.stdout}")
            return
        else:
            await update.message.reply_text(f"Error:\n{result.stderr}")
            return
    except Exception as e:
        await update.message.reply_text(f"Exception: {e}")


async def down(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        result, cmd = send_down()
        if result.returncode == 0:
            await update.message.reply_text(f"Stopped:\n{cmd}\nOutput:\n{result.stdout}")
            return
        else:
            await update.message.reply_text(f"Error:\n{result.stderr}")
            return
    except Exception as e:
        await update.message.reply_text(f"Exception: {e}")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if True: #user_id in username_list:
        help_message = "Here are the available commands:\n"
        help_message += "/start - Start a selected save for Factorio\n"
        help_message += "/down - Stop the Factorio server for now\n"
        help_message += "/list - List all the saves available on the server\n"
        help_message += "/help - Shows you all the available commands\n"
        await update.message.reply_text(f"{help_message}")
    else:
        help_message = "Voici la liste des commandes disponibles :\n"
        help_message += "/start - Démarre le bot et affiche un message de bienvenue.\n"
        help_message += "/inscription - Permet de s'inscrire au créneau de volley de Bordeaux INP.\n"
        await update.message.reply_text(help_message)


def main() -> None:
    # Créez l'application avec votre token d'API
    app = Application.builder().token(TOKEN).build()

    # Ajoutez des gestionnaires de commandes
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("down", down))
    app.add_handler(CommandHandler("help", help))

    # Démarrez l'application
    app.run_polling()


if __name__ == '__main__':
    main()
