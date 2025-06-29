from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import subprocess

from utils.commands import *

load_dotenv(".telegram-env")

TOKEN = os.getenv("TOKEN")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}'
                                    )


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
                await update.message.reply_text(
                    "Invalid argument. Please try again.")
                return

        # If this is a reply with a number
        elif update.message.text.isdigit():
            saves_number = int(update.message.text)
            if 0 <= saves_number < len(ls):
                save_name = ls[saves_number]
            else:
                await update.message.reply_text(
                    "Invalid number. Please try again.")
                return
        else:
            await update.message.reply_text(mess)
            return

        cmd = f"SAVE_NAME={save_name} docker compose up -d"
        result = subprocess.run(cmd,
                                shell=True,
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            await update.message.reply_text(
                f"Started:\n{cmd}\nOutput:\n{result.stdout}")
            return
        else:
            await update.message.reply_text(f"Error:\n{result.stderr}")
            return
    except Exception as e:
        await update.message.reply_text(f"Exception: {e}")


async def down(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cmd = f"docker compose down"
    try:
        result = subprocess.run(cmd,
                                shell=True,
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            await update.message.reply_text(
                f"Stopped:\n{cmd}\nOutput:\n{result.stdout}")
            return
        else:
            await update.message.reply_text(f"Error:\n{result.stderr}")
            return
    except Exception as e:
        await update.message.reply_text(f"Exception: {e}")


def main() -> None:
    # Créez l'application avec votre token d'API
    app = Application.builder().token(TOKEN).build()

    # Ajoutez des gestionnaires de commandes
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", down))

    # Démarrez l'application
    app.run_polling()


if __name__ == '__main__':
    main()
