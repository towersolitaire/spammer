import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import schedule
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Your Telegram API details
api_id = '19463194'
api_hash = 'bf73819bc78d6d974c40fe27bc5fffe9'
phone_number = '+447442868720'

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# List of chat IDs to send the message to
chat_ids = [
    -1001312163180, -1001810102855, -1001159814045, -1002114471760,
    -1001936718362, -1002024414792, -1001902027966, -1001374159651,
    -1001256452830, -1002094448369, -1001680799362, 6331702584, -1002092360620, -1001489331297
]


# ID to send error notifications and start confirmation to
notification_id = 535400200

# The message you want to send
message_text = """
Пропонуємо роботу❗️
📦Комірник
🚚Водій категорії В (з досвідом від 1 року)
👷‍♂️Водій автонавантажувача (обов'язкова наявність посвідчення водія навантажувача)
🇺🇦KABLEX UKRAINE🇺🇦 
Кабельне підприємство
💰Від 18000 до 25000грн;
📍Київське шосе, 10б (біля Нової Лінії);
🚍Доставка на роботу транспортом підприємства;
🕒Графік роботи: 
Пн-пт -повний робочий день, 
Сб — до 13:00/14:00 годин;
☎️ 0639982527 Олександр. Телефонуйте або пишіть!
"""

# Simple HTTP server for Adaptable.io
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"I'm alive!")

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP server running on port {port}")
    httpd.serve_forever()

async def send_message():
    async with client:
        for chat_id in chat_ids:
            try:
                await client.send_message(chat_id, message_text)
                print(f"Message sent to {chat_id}")
            except FloodWaitError as e:
                print(f"Flood wait error: {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Error sending to {chat_id}: {e}")
                await client.send_message(notification_id, f"Error sending to {chat_id}: {e}")

async def notify_start():
    async with client:
        try:
            await client.send_message(notification_id, "Script started successfully and is running.")
            print(f"Start notification sent to {notification_id}")
        except Exception as e:
            print(f"Error sending start notification: {e}")

def schedule_jobs():
    # Schedule messages from 08:35 to 21:35 every hour
    for hour in range(8, 22):  # From 8 to 21 inclusive
        time_str = f"{hour:02d}:35"
        schedule.every().day.at(time_str).do(lambda: asyncio.create_task(send_message()))

# Event handler to respond to messages from the notification_id
@client.on(events.NewMessage(chats=notification_id))
async def handler(event):
    try:
        await event.reply("i’m working")
        print("Replied to message from notification_id")
    except Exception as e:
        print(f"Error replying to {notification_id}: {e}")

async def main():
    await notify_start()
    schedule_jobs()

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Start the client and run the script
if name == "__main__":
    client.start(phone=phone_number)
    
    # Start the HTTP server in a separate thread
    import threading
    threading.Thread(target=run_http_server).start()
    
    client.loop.run_until_complete(main())
