from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
import os
from dotenv import load_dotenv
import subprocess

from utils.commands import *

load_dotenv(".telegram-env")

TOKEN = os.getenv("TOKEN")
ADMINS:List[int] = [] #os.getenv("ADMINS")
if os.getenv("ADMINS"):
    ADMINS = [int(user_id.strip()) for user_id in os.getenv("ADMINS").split(",")]



async def hello(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def list(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    ls = get_saves_list()
    await update.message.reply_text(f'the list of saves is {ls}')


async def start(update, context):

    user_id = update.message.from_user.id
    if user_id in ADMINS:
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

    user_id = update.message.from_user.id
    if user_id in ADMINS:
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
    if user_id in ADMINS:
        help_message = "Here are the available commands:\n"
        help_message += "/start - Start a selected save for Factorio\n"
        help_message += "/down - Stop the Factorio server for now\n"
        help_message += "/list - List all the saves available on the server\n"
        help_message += "/help - Shows you all the available commands\n"
        help_message += "/shutdown shuts down the server \n"
        help_message += "/restart let you restart the server \n"
        await update.message.reply_text(f"{help_message}")
    else:
        help_message = "Here are the available commands:\n"
        help_message += "/list - List all the saves available on the server\n"
        help_message += "/help - Shows you all the available commands\n"
        await update.message.reply_text(f"{help_message}")


async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMINS[0]:
        cmd = "shutdown now"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            await update.message.reply_text(f"Server is shutting down.\nCommand: {cmd}\nOutput:\n{result.stdout}")
        else:
            await update.message.reply_text(f"Failed to shut down the server.\nCommand: {cmd}\nError:\n{result.stderr}")
        return


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id in ADMINS:
        cmd = "reboot"
        return subprocess.run(cmd, shell=True, capture_output=True, text=True), cmd



def main() -> None:
    # Créez l'application avec votre token d'API
    app = Application.builder().token(TOKEN).build()

    # Ajoutez des gestionnaires de commandes
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("down", down))
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("restart", restart))

    # Démarrez l'application
    app.run_polling()


if __name__ == '__main__':
    main()
