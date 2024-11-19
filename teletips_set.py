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


@bot.on_message(filters.command('set') & (filters.group | filters.private))
@bot.on_channel_post(filters.regex(r'^/set \d+ ".*"$'))
async def set_timer(client, message):
    global stoptimer
    try:
        # Обробка для каналів
        if message.chat.type == "channel":
            command_parts = message.text.split(" ", 2)
            if len(command_parts) < 3:
                return await client.send_message(
                    message.chat.id,
                    '❌ **Некоректний формат.**\n\n✅ Формат:\n<code>/set секунди "подія"</code>\n\n**Приклад**:\n<code>/set 10 "Таймер на 10 секунд"</code>'
                )

            user_input_time = int(command_parts[1])
            user_input_event = command_parts[2].strip('"')
            sent_message = await client.send_message(message.chat.id, "⏳ Таймер встановлено!")
        else:
            # Перевірка прав адміністратора для груп
            user_member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if not user_member.privileges:
                return await message.reply("👮🏻‍♂️ Вибачте, тільки адміністратори можуть виконувати цю команду.")

            # Перевірка на коректність формату команди
            if len(message.command) < 3:
                return await message.reply('❌ **Некоректний формат.**\n\n✅ Формат:\n<code>/set секунди "подія"</code>\n\n**Приклад**:\n<code>/set 10 "Таймер на 10 секунд"</code>')

            user_input_time = int(message.command[1])
            user_input_event = str(message.command[2])
            sent_message = await client.send_message(message.chat.id, "⏳ Таймер встановлено!")

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
        if message.chat.type == "channel":
            await client.send_message(message.chat.id, f"⚠️ Помилка: {str(e)}")
        else:
            await message.reply(f"⚠️ Помилка: {str(e)}")


@bot.on_message(filters.command('stopc') & (filters.group | filters.private))
@bot.on_channel_post(filters.regex(r'^/stopc$'))
async def stop_timer(client, message):
    global stoptimer
    try:
        if message.chat.type != "channel":
            user_member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if not user_member.privileges:
                return await message.reply("👮🏻‍♂️ Вибачте, тільки адміністратори можуть виконувати цю команду.")
        stoptimer = True
        await client.send_message(message.chat.id, "🛑 Відлік зупинено.")
    except FloodWait as e:
        await asyncio.sleep(e.value)


print("Countdown Timer Bot is running!")
bot.run()
