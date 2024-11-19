from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram.errors import FloodWait

bot = Client(
    "Countdown-TeLeTiPs",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

footer_message = os.environ["FOOTER_MESSAGE"]
stoptimer = False


@bot.on_channel_post(filters.regex(r'^/set \d+ ".*"$'))
async def set_timer_channel(client, message: Message):
    global stoptimer
    try:
        # Розділення команди на параметри
        command_parts = message.text.split(" ", 2)
        if len(command_parts) < 3:
            return await client.send_message(
                message.chat.id,
                '❌ **Некоректний формат.**\n\n✅ Формат:\n<code>/set секунди "подія"</code>\n\n**Приклад**:\n<code>/set 10 "Таймер на 10 секунд"</code>'
            )

        user_input_time = int(command_parts[1])
        user_input_event = command_parts[2].strip('"')

        sent_message = await client.send_message(message.chat.id, f"⏳ Таймер: {user_input_event}")

        stoptimer = False

        # Основний цикл таймера
        while user_input_time > 0 and not stoptimer:
            d, h, m, s = (
                user_input_time // (3600 * 24),
                user_input_time % (3600 * 24) // 3600,
                user_input_time % 3600 // 60,
                user_input_time % 60,
            )
            countdown_text = f'{user_input_event}\n\n⏳ {d}**д** {h:02d}**г** {m:02d}**хв** {s:02d}**с**\n\n<i>{footer_message}</i>'
            await sent_message.edit_text(countdown_text)
            await asyncio.sleep(3 if user_input_time > 10 else 1)
            user_input_time -= 3 if user_input_time > 10 else 1

        if not stoptimer:
            await sent_message.edit_text("🚨 Beep! Beep!! **Час вийшов!!!**")
        else:
            await sent_message.edit_text("🛑 Відлік зупинено.")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await client.send_message(message.chat.id, f"⚠️ Помилка: {str(e)}")


@bot.on_channel_post(filters.regex(r'^/stopc$'))
async def stop_timer_channel(client, message: Message):
    global stoptimer
    try:
        stoptimer = True
        await client.send_message(message.chat.id, "🛑 Відлік зупинено.")
    except FloodWait as e:
        await asyncio.sleep(e.value)


print("Countdown Timer Bot is running!")
bot.run()
