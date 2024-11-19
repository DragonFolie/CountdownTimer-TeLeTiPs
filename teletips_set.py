from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from pyrogram.errors import FloodWait, MessageNotModified

bot = Client(
    "Countdown-TeLeTiPs",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

footer_message = os.environ["FOOTER_MESSAGE"]
stoptimer = False

TELETIPS_MAIN_MENU_BUTTONS = [
    [
        InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")
    ],
    [
        InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
        InlineKeyboardButton('📣 CHANNEL', url='https://t.me/teletipsofficialchannel'),
        InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/teIetips')
    ],
    [
        InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")
    ]
]


@bot.on_message(filters.command(['start', 'help']) & filters.private)
async def start(client, message):
    text = "👋 Welcome to Countdown Timer Bot!"
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data == "HELP_CALLBACK":
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
        ])
        try:
            await query.edit_message_text(
                "ℹ️ This bot helps you create countdowns in Telegram chats and channels.",
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
    elif query.data == "GROUP_CALLBACK":
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("TeLe TiPs Chat [EN]", url="https://t.me/teletipsofficialontopicchat")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
        ])
        try:
            await query.edit_message_text(
                "👥 Join our support group for more help.",
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
    elif query.data == "TUTORIAL_CALLBACK":
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 Video", url="https://youtu.be/nYSrgdIYdTw")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
        ])
        try:
            await query.edit_message_text(
                "🎓 Learn how to create your own bot with this tutorial.",
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
    elif query.data == "START_CALLBACK":
        reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
        try:
            await query.edit_message_text(
                "👋 Welcome to Countdown Timer Bot!",
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


@bot.on_message(filters.command('set'))
async def set_timer(client, message):
    global stoptimer
    try:
        if message.chat.type in ['supergroup', 'group', 'channel']:
            chat_member = await client.get_chat_member(message.chat.id, client.me.id)
            if not chat_member.privileges or not chat_member.privileges.can_post_messages:
                return await message.reply('❌ Бот не має прав на публікацію повідомлень.')
        else:
            return await message.reply('⛔️ Команда доступна тільки в групах та каналах.')

        if message.chat.type != 'channel':
            user_member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if not user_member.privileges:
                return await message.reply('👮🏻‍♂️ Вибачте, тільки адміністратори можуть виконувати цю команду.')

        if len(message.command) < 3:
            return await message.reply('❌ **Некоректний формат.**\n\n✅ Формат:\n<code> /set секунди "подія"</code>\n\n**Приклад**:\n <code>/set 10 "Зворотний відлік на 10 секунд"</code>')

        user_input_time = int(message.command[1])
        user_input_event = str(message.command[2])
        get_user_input_time = await client.send_message(message.chat.id, user_input_time)
        stoptimer = False

        while user_input_time > 0 and not stoptimer:
            d, h, m, s = (
                user_input_time // (3600 * 24),
                user_input_time % (3600 * 24) // 3600,
                user_input_time % 3600 // 60,
                user_input_time % 60,
            )
            countdown_text = f'{user_input_event}\n\n⏳ {d}**д** {h:02d}**г** {m:02d}**хв** {s:02d}**с**\n\n<i>{footer_message}</i>'
            await get_user_input_time.edit(countdown_text)
            await asyncio.sleep(3 if user_input_time > 10 else 1)
            user_input_time -= 3 if user_input_time > 10 else 1

        if not stoptimer:
            await get_user_input_time.edit("🚨 Beep! Beep!! **Час вийшов!!!**")
        else:
            await get_user_input_time.edit("🛑 Відлік зупинено.")

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"⚠️ Помилка: {str(e)}")


@bot.on_message(filters.command('stopc'))
async def stop_timer(client, message):
    global stoptimer
    try:
        if message.chat.type != 'channel':
            user_member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if not user_member.privileges:
                return await message.reply('👮🏻‍♂️ Вибачте, тільки адміністратори можуть виконувати цю команду.')
        stoptimer = True
        await message.reply('🛑 Відлік зупинено.')
    except FloodWait as e:
        await asyncio.sleep(e.value)


print("Countdown Timer Bot is running!")
bot.run()
