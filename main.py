import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import logging
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
START, FETCH_MESSAGES = range(2)

# Bot token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7880934596:AAG7_DAoSg6MDyB2sQ8jfc6NWX6TQoTBRgI")
WAIT = os.environ.get("WAIT", "3")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Please provide the following details to start copying messages:\n"
        "1. Source Channel ID\n"
        "2. Target Channel ID\n"
        "3. Starting Message ID\n"
        "4. Ending Message ID"
    )
    return START

# Fetch and copy messages
async def fetch_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract user inputs
        user_data = update.message.text.split()
        if len(user_data) != 4:
            await update.message.reply_text("Please provide exactly 4 values (source_id, target_id, start_id, end_id).")
            return START

        source_channel_id = user_data[0]
        target_channel_id = user_data[1]
        start_id = int(user_data[2])
        end_id = int(user_data[3])

        bot = context.bot
        for msg_id in range(start_id, end_id + 1):
            try:
                message = await bot.get_chat(source_channel_id).get_message(msg_id)

                if message.video:
                    await bot.send_video(
                        chat_id=target_channel_id,
                        video=message.video.file_id,
                        caption="BY OPMASTER"
                    )
                elif message.photo:
                    await bot.send_photo(
                        chat_id=target_channel_id,
                        photo=message.photo[-1].file_id,  # Best quality
                        caption="𝐁𝐘 𝐃𝐀𝐑𝐊 𝐍𝐈𝐆𝐇𝐓 🌟 - [@DARKCOLLECT_BOT]"
                    )
                elif message.document:
                    await bot.send_document(
                        chat_id=target_channel_id,
                        document=message.document.file_id,
                        caption="𝐁𝐘 𝐃𝐀𝐑𝐊 𝐍𝐈𝐆𝐇𝐓 🌟 - [@DARKCOLLECT_BOT]"
                    )
                elif message.animation:
                    await bot.send_animation(
                        chat_id=target_channel_id,
                        animation=message.animation.file_id,
                        caption="𝐁𝐘 𝐃𝐀𝐑𝐊 𝐍𝐈𝐆𝐇𝐓 🌟 - [@DARKCOLLECT_BOT]"
                    )
                else:
                    await bot.copy_message(
                        chat_id=target_channel_id,
                        from_chat_id=source_channel_id,
                        message_id=msg_id
                    )

                await asyncio.sleep(int(WAIT))
            except Exception as e:
                logger.error(f"Error copying message {msg_id}: {e}")
                continue

        await update.message.reply_text("Messages copied successfully!")
    except ValueError:
        await update.message.reply_text("Invalid input. Ensure that message IDs are integers.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("An error occurred while processing your request.")
    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Main function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_messages)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
