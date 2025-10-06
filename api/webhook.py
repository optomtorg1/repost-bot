import os
import asyncio
from aiohttp import web
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

# ⚙️ Переменные окружения в Vercel Dashboard
BOT_TOKEN = os.getenv("8345607034:AAF6eEPTR0aMxxaRbxehJqPGw05LO1Kzca4")
SOURCE_CHANNEL_ID = int(os.getenv("-1002579803044"))  # канал, откуда репостим
TARGET_CHAT_ID = int(os.getenv("-1002869860411"))        # группа, куда репостим

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def handle(request):
    # Получаем параметр message_id из URL
    params = request.rel_url.query
    msg_id = params.get("message_id")
    
    if not msg_id:
        return web.Response(text="❌ Укажи параметр message_id, например ?message_id=123")
    
    try:
        msg_id = int(msg_id)
        await bot.copy_message(
            chat_id=TARGET_CHAT_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=msg_id
        )
        return web.Response(text=f"✅ Сообщение {msg_id} успешно переслано!")
    except Exception as e:
        return web.Response(text=f"❌ Ошибка: {e}")

# Создаем aiohttp приложение
async def init():
    app = web.Application()
    app.router.add_get("/", handle)  # GET-запрос
    app.router.add_post("/", handle) # POST-запрос
    return app

app = asyncio.run(init())
