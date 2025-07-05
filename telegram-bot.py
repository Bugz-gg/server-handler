from typing import List
import zipfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater, ConversationHandler
import os
from dotenv import load_dotenv
import subprocess

from utils.commands import *

load_dotenv(".telegram-env")

UPLOAD_ZIP = range(1)
TOKEN = os.getenv("TOKEN")
ADMINS:List[str] = [] #os.getenv("ADMINS")
if os.getenv("ADMINS"):
    ADMINS = [user_id.strip() for user_id in os.getenv("ADMINS").split(",")]



async def hello(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def list(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    ls = get_saves_list()
    await update.message.reply_text(f'the list of saves is {ls}')


async def start(update, context):

    user_id = update.message.from_user.id
    if str(user_id) in ADMINS:
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
    if str(user_id) in ADMINS:
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

async def upload_factorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id) # Corrected from user.idd to user.id

    if user_id in ADMINS:
        await update.message.reply_text("Please upload the Factorio save ZIP file now.")
        return UPLOAD_ZIP # Enter the UPLOAD_ZIP state
    else:
        await update.message.reply_text("You are not authorized to upload saves.")
        return ConversationHandler.END # End the conversation if not authorized

async def receive_zip_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)

    if user_id in ADMINS:
        if update.message.document and update.message.document.mime_type == 'application/zip':
            # Download file to temp location
            file = await update.message.document.get_file()
            temp_path = f"/tmp/{update.message.document.file_name}"
            await file.download_to_drive(temp_path) # Corrected awaitfile.downloadad_to_drive to await file.download_to_drive

            # Check if it's a valid zip file (using os.path.exists for safety before zipfile check)
            if os.path.exists(temp_path) and zipfile.is_zipfile(temp_path): # Corrected zipfile.zipfile.is to zipfile.is_zipfile
                try:
                    # Extract to server directory
                    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                        # It's good practice to ensure the target directory exists
                        os.makedirs('/opt/factorio/saves/', exist_ok=True)
                        zip_ref.extractall('/opt/factorio/saves/')
                    await update.message.reply_text("Upload and extraction successful.")
                except Exception as e:
                    await update.message.reply_text(f"Extraction failed: {e}")
                finally:
                    os.remove(temp_path) # Clean up temp file
            else:
                await update.message.reply_text("The file is not a valid ZIP archive.")
        else:
            await update.message.reply_text("That doesn't look like a ZIP file. Please upload a ZIP file.")
    else:
        # This case should ideally not be reached if ConversationHandler is set up correctly,
        # but as a safeguard:
        await update.message.reply_text("You are not authorized to upload saves.")

    return ConversationHandler.END # End the conversation

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Upload process cancelled."
    )
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if str(user_id) in ADMINS:
        help_message = "Here are the available commands:\n"
        help_message += "/start - Start a selected save for Factorio\n"
        help_message += "/down - Stop the Factorio server for now\n"
        help_message += "/list - List all the saves available on the server\n"
        help_message += "/help - Shows you all the available commands\n"
        help_message += "/shutdown shuts down the server \n"
        help_message += "/restart let you restart the server \n"
        help_message += "/upload to upload zip save \n"
        await update.message.reply_text(f"{help_message}")
    else:
        help_message = "Here are the available commands:\n"
        help_message += "/list - List all the saves available on the server\n"
        help_message += "/help - Shows you all the available commands\n"
        await update.message.reply_text(f"{help_message}")


async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.from_user.id) == ADMINS[0]:
        cmd = "shutdown now"
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.from_user.id) in ADMINS:
        cmd = "reboot"
        return subprocess.run(cmd, shell=True, capture_output=True, text=True), cmd



def main() -> None:
    # Create the application with your API token
    app = Application.builder().token(TOKEN).build()

    # Add command handlers for your regular commands
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("down", down))
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("restart", restart))

    # --- Conversation Handler for the 'upload' command ---
    # This replaces the single CommandHandler("upload", send_upload_factorio)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("upload", upload_factorio)], # Starts the conversation
        states={
            UPLOAD_ZIP: [
                # Handles the ZIP file upload when in the UPLOAD_ZIP state
                MessageHandler(filters.Document.ZIP, receive_zip_file),
                # Fallback for non-ZIP messages in the UPLOAD_ZIP state
                MessageHandler(
                    filters.ALL & ~filters.COMMAND,
                    lambda u, c: u.message.reply_text("Please send a ZIP file or /cancel to stop the upload process.")
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)], # Allows users to cancel the upload at any point
    )

    # Add the ConversationHandler to your application
    app.add_handler(conv_handler)

    # Start the application
    print("Bot started. Press Ctrl-C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
