from fastapi import FastAPI, Request
import os
import asyncio
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

BOT_TOKEN = "8345607034:AAF6eEPTR0aMxxaRbxehJqPGw05LO1Kzca4"
SOURCE_CHANNEL_ID = -2579803044
TARGET_CHAT_ID = -1009876543210

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

app = FastAPI()

@app.get("/")
async def webhook(request: Request):
    msg_id = request.query_params.get("message_id")
    if not msg_id:
        return {"error": "Укажи параметр message_id, например ?message_id=123"}

    try:
        msg_id = int(msg_id)
        await bot.copy_message(
            chat_id=TARGET_CHAT_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=msg_id
        )
        return {"success": f"Сообщение {msg_id} успешно переслано!"}
    except Exception as e:
        return {"error": str(e)}
