from telethon import TelegramClient, events
from flask import Flask
import threading

# --- Flask для Railway Domains ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot for *6756 is alive ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Telegram API ---
api_id = 21656727
api_hash = '561e1c275ae2a89cc2b8670bb1a3a178'

client = TelegramClient('forwarder_session_6756', api_id, api_hash)

target_group_id = -4720268824
source_bot_username = 'HUMOcardbot'

# Множество для хранения хэшей обработанных сообщений
handled_messages = set()

@client.on(events.NewMessage(from_users=source_bot_username))
async def handler(event):
    text = event.raw_text.strip()
    message_hash = hash(text)

    # Фильтрация: только пополнение по карте *6756 и ещё не отправлялось
    if message_hash not in handled_messages and '🎉 Пополнение' in text and '💳 HUMOCARD *6756' in text:
        handled_messages.add(message_hash)

        # Форматируем жирный текст
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if '🎉 Пополнение' in line or '➕' in line:
                line = f"<b>{line}</b>"
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)
        custom_message = f"<b>AUA</b>\n{formatted_text}"

        await client.send_message(target_group_id, custom_message, parse_mode='html')

# --- Запуск Flask и Telethon ---
threading.Thread(target=run_flask).start()
client.start()
print("Userbot for *6756 is running ✅")
client.run_until_disconnected()
