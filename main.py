from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import html
import asyncio
# Replace with your bot token
BOT_TOKEN = "8104493069:AAHVHGeNtiD4_vtfwy0z9XydKBG_h1UiA00"

# Function to get token from the URL
def get_token_from_url():
    url = "https://pickupbaby.koyeb.app/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

# Fetch token for API requests
TOKEN = get_token_from_url()

def get_user_id_to_idx():
    url = "https://userdataupdate.koyeb.app/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return {}

USER_ID_TO_IDX = get_user_id_to_idx()  # Automatic fetching of user IDs and phone numbers

# Year-Class-Batch Mapping
YEAR_CLASSES = {
    "2024-25": {
        "11th": {
            "Vijay 2.0(PCM)": "98",
            "Vijay 3.0(PCM)": "110",
            "Vijay 4.0(PCM)": "116",
            "Vijay 5.0(PCM)": "119",
            
        },
        "12th": {
            "Vijeta 2.0 Chem Spl": "89",
            "Vijeta 4.0 (PCM)": "99",            
        },
        "13th": {
             "Vishesh 2.0 (PCM)": "100",
             "Vishesh 3.0 (PCM)": "108",
             "Vishesh 4.0 (PCM)": "114",
             "Vishesh 5.0 (PCM)": "117",
             
         },    
        
        "CrashCourse": {
            "Adv Ranker (PCM)": "94",
            "Victroy 1.0 (PCM)": "123",
            "Test Series (PCM)": "124",
            },            
    },
    "2025-26": {
        "11th": {
            "Backlog Silver Chem": "131",
            "Vijeta 1.0 Gold (11+12) Chem": "132",
            "Vijeta 1.0 Silver (11+12) Chem": "133",
            "Vijeta 1.0 Diamond (11+12) Chem": "134",
        },
        "12th": {
            "Vijeta 1.0 Silver (PCM)": "126",
            "Vijeta 1.0 GOLD (PCM)": "128",
            "Vijeta 1.0 Diamond (PCM)": "130",
            "Vijeta 1.0 Gold (11+12) Chem": "132",
            "Vijeta 1.0 Silver (11+12) Chem": "133",
            "Vijeta 1.0 Diamond (11+12) Chem": "134",
        },
         "CrashCourse": {
            "JEE MAINS CC - 2 Attmpt": "135",
            "JEE ADV CC 2025": "136",
            "JEE (M+ADV) 2025": "137",
            "GOC (11th + 12th)": "138",
            },            
    },
}

# Mapping of Telegram user IDs to phone numbers

# Fetch subjects
def fetch_subjects(batch_id):
    url = f"https://spec.iitschool.com/api/v1/batch-subject/{batch_id}"
    headers = {"Accept": "application/json", "origintype": "web", "token": TOKEN, "usertype": "2"}
    response = requests.get(url, headers=headers)
    return response.json()["data"]["batch_subject"] if response.status_code == 200 and response.json()["responseCode"] == 200 else []

# Fetch topics
def fetch_topics(batch_id, subject_id):
    url = f"https://spec.iitschool.com/api/v1/batch-topic/{subject_id}?type=class"
    headers = {"Accept": "application/json", "origintype": "web", "token": TOKEN, "usertype": "2"}
    response = requests.get(url, headers=headers)
    return response.json()["data"]["batch_topic"] if response.status_code == 200 and response.json()["responseCode"] == 200 else []

# Fetch lessons
def fetch_lessons(batch_id, subject_id, topic_id):
    url = f"https://spec.iitschool.com/api/v1/batch-detail/{batch_id}?subjectId={subject_id}&topicId={topic_id}"
    headers = {"Accept": "application/json", "origintype": "web", "token": TOKEN, "usertype": "2"}
    response = requests.get(url, headers=headers)
    return response.json()["data"]["class_list"]["classes"] if response.status_code == 200 and response.json()["responseCode"] == 200 else []

# Fetch notes
def fetch_notes(batch_id, subject_id, topic_id):
    url = f"https://spec.iitschool.com/api/v1/batch-notes/{batch_id}?subjectId={subject_id}&topicId={topic_id}"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["responseCode"] == 200:
            return data["data"]["notesDetails"]
    return []


# Start command
async def check_for_updates(context: ContextTypes.DEFAULT_TYPE):
    global TOKEN, USER_ID_TO_IDX
    
    new_token = get_token_from_url()
    new_user_idx = get_user_id_to_idx()
    
    if new_token != TOKEN:
        TOKEN = new_token
        print("Token updated.")
    
    if new_user_idx != USER_ID_TO_IDX:
        USER_ID_TO_IDX = new_user_idx
        print("User index updated.")

    # Run every minute
    context.job_queue.run_once(check_for_updates, 20)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id not in USER_ID_TO_IDX:
        await update.message.reply_text("<b>❌ 𝐀𝐚𝐫𝐞 𝐰𝐚𝐚𝐡 𝐁𝐄𝐓𝐈𝐂𝐇𝐎𝐃 𝐟𝐫𝐞𝐞 𝐤𝐚 𝐥𝐞𝐧𝐞 𝐚𝐚𝐲𝐚 𝐡𝐚𝐢 𝐤𝐲𝐚 🤣 𝐛𝐡𝐚𝐤\n\n✥ Yaha Msg kar Aur kharidle bhai kyu mara raha hai 😔\n𝐂𝐎𝐍𝐓𝐀𝐂𝐓 - @NITSCHOOL_BOT</b>", parse_mode="HTML", protect_content="True")
        return

    keyboard = [
        [InlineKeyboardButton("𝟐𝟎𝟐𝟒 ✦ 𝟐𝟎𝟐𝟓", callback_data="year_2024-25")],
        [InlineKeyboardButton("𝟐𝟎𝟐𝟓 ✦ 𝟐𝟎𝟐𝟔", callback_data="year_2025-26")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📅 <b>Select Which Year Batches You want 😁</b>", parse_mode="HTML", protect_content="True", reply_markup=reply_markup)

# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(query.from_user.id)

    if user_id not in USER_ID_TO_IDX:
        await query.edit_message_text("<b>❌ 𝐀𝐚𝐫𝐞 𝐰𝐚𝐚𝐡 𝐁𝐄𝐓𝐈𝐂𝐇𝐎𝐃 𝐟𝐫𝐞𝐞 𝐤𝐚 𝐥𝐞𝐧𝐞 𝐚𝐚𝐲𝐚 𝐡𝐚𝐢 𝐤𝐲𝐚 🤣 𝐛𝐡𝐚𝐤\n\n✥ Yaha Msg kar Aur kharidle bhai kyu mara raha hai 😔\n𝐂𝐎𝐍𝐓𝐀𝐂𝐓 - @NITSCHOOL_BOT</b>", parse_mode="HTML")
        return

    if data.startswith("year_"):
        year = data.split("_")[1]
        keyboard = [[InlineKeyboardButton(cls, callback_data=f"class_{year}_{cls}")] for cls in YEAR_CLASSES[year]]
        await query.edit_message_text(f"📚 <b>Select your class for {year}:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("class_"):
        _, year, class_name = data.split("_")
        batches = YEAR_CLASSES[year][class_name]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"batch_{batch_id}")] for name, batch_id in batches.items()]
        await query.edit_message_text("📂 <b>Select a batch: </b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("batch_"):
        batch_id = data.split("_")[1]
        subjects = fetch_subjects(batch_id)
        keyboard = [[InlineKeyboardButton(subject["subjectName"], callback_data=f"subject_{batch_id}_{subject['id']}")] for subject in subjects]
        await query.edit_message_text("📖 <b>Select a subject:</b>\n\n", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("subject_"):
        _, batch_id, subject_id = data.split("_")
        topics = fetch_topics(batch_id, subject_id)
        keyboard = [[InlineKeyboardButton(topic["topicName"], callback_data=f"topic_{batch_id}_{subject_id}_{topic['id']}")] for topic in topics]
        await query.edit_message_text("📌 <b>Select a topic:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("topic_"):
        _, batch_id, subject_id, topic_id = data.split("_")
        lessons = fetch_lessons(batch_id, subject_id, topic_id)
        notes = fetch_notes(batch_id, subject_id, topic_id)
        phone_number = USER_ID_TO_IDX[user_id]

        keyboard = [
            [InlineKeyboardButton(lesson["lessonName"], url=f'https://vercelsop.vercel.app/{phone_number}/{lesson["id"]}')] for lesson in lessons
        ]

        if notes:
                keyboard.append([InlineKeyboardButton("Notes", callback_data=f"notes_{batch_id}_{subject_id}_{topic_id}")])
                reply_markup = InlineKeyboardMarkup(keyboard)
        # Edit message with web preview enabled
                await query.edit_message_text(
                text="Select a lesson or view notes:",
                reply_markup=reply_markup,
                disable_web_page_preview=False  # Enable web preview
        )
        elif notes:
            notes_message = "\n\n".join([
                f"🌟<a href=\"{html.escape(note['docUrl'])}\">{html.escape(note['docTitle'])}</a>"
                for note in notes
            ])
            await query.edit_message_text(
                text=(
                    "<b> 𝐀𝐋𝐋 𝐍𝐎𝐓𝐄𝐒 𝐁𝐄𝐋𝐎𝐖 👇</b>\n"
                    "----------------------------------------------------------\n\n"
                    f"<b>{notes_message}</b>\n"
                    "----------------------------------------------------------\n\n"
                    "<b>𝗠𝗮𝗱𝗲 𝗕𝘆 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 😈</b>\n"
                    "CONTACT US - @NITSCHOOL_BOT\n\n"
                    "You Are on Last page for more Lectures,Notes - /start"
                ),
                parse_mode="HTML",
                disable_web_page_preview=False  # Enable web preview
            )
        else:
            await query.edit_message_text(text="Sorry isme Lectures aur Notes nahi hai abhi")

    elif data.startswith("notes_"):
        _, batch_id, subject_id, topic_id = data.split("_")
        notes = fetch_notes(batch_id, subject_id, topic_id)
        if notes:
            notes_message = "\n\n".join([f"🌟<a href=\"{html.escape(note['docUrl'])}\">{html.escape(note['docTitle'])}</a>" for note in notes])
            await query.edit_message_text(text=f"<b> 𝐀𝐋𝐋 𝐍𝐎𝐓𝐄𝐒 𝐁𝐄𝐋𝐎𝐖 👇</b>\n----------------------------------------------------------\n\n<b>{notes_message}</b>\n----------------------------------------------------------\n\n<b>𝗠𝗮𝗱𝗲 𝗕𝘆 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 😈</b>\nCONTACT US - @NITSCHOOL_BOT\n\nYou Are on Last page for more Lectures,Notes - /start",
            parse_mode="HTML"
            )
        else:
            await query.edit_message_text(text="Sorry Notes nahi hai isme 😔.")
# Main function
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Add job queue
    job_queue = application.job_queue
    job_queue.run_once(check_for_updates, 20)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

# Run bot
if __name__ == "__main__":
    main()
