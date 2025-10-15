import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
import pandas as pd
import aiohttp
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("8492898268:AAExZz9nPousVK4OvbN0d1wqHdhkKXqaMxQ")
API_KEY = os.getenv("ABC123XYZ456")
FX_BASE = os.getenv("FX_BASE", "EUR")
FX_QUOTE = os.getenv("FX_QUOTE", "USD")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def make_menu():
    kb = [
        [InlineKeyboardButton("📊 Start 2-min signals", callback_data="start_2m")],
        [InlineKeyboardButton("⏱ Start 5-min signals", callback_data="start_5m")],
        [InlineKeyboardButton("🛑 Stop signals", callback_data="stop")],
        [InlineKeyboardButton("📁 Get logs", callback_data="get_logs")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🚀 Forex Signal Bot is ready!", reply_markup=make_menu())

tasks = {}

async def fetch_data(pair, interval):
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={FX_BASE}&to_symbol={FX_QUOTE}&interval=1min&apikey={API_KEY}&datatype=csv"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            df = pd.read_csv(pd.compat.StringIO(text))
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.sort_values("timestamp", inplace=True)
            return df.tail(20)

def analyze(df):
    df["ema_fast"] = df["close"].ewm(span=5).mean()
    df["ema_slow"] = df["close"].ewm(span=14).mean()
    if df["ema_fast"].iloc[-1] > df["ema_slow"].iloc[-1]:
        return "BUY"
    else:
        return "SELL"

async def signal_loop(message: types.Message, interval):
    user_id = message.chat.id
    while user_id in tasks:
        df = await fetch_data(f"{FX_BASE}/{FX_QUOTE}", interval)
        signal = analyze(df)
        now = datetime.utcnow().strftime("%H:%M:%S")
        await message.answer(f"💹 {FX_BASE}/{FX_QUOTE} | {interval} | Signal: {signal} | {now}")
        await asyncio.sleep(interval * 60)

@dp.callback_query()
async def callbacks(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data.startswith("start_"):
        if user_id in tasks:
            await call.message.answer("⚠️ Signals already running.")
            return
        interval = 2 if "2m" in call.data else 5
        tasks[user_id] = asyncio.create_task(signal_loop(call.message, interval))
        await call.message.answer(f"✅ Started {interval}-min signals.")

    elif call.data == "stop":
        if user_id in tasks:
            tasks[user_id].cancel()
            del tasks[user_id]
            await call.message.answer("🛑 Signals stopped.")
        else:
            await call.message.answer("ℹ️ No active signals.")

    elif call.data == "get_logs":
        if os.path.exists("signals_log.csv"):
            await call.message.answer_document(open("signals_log.csv", "rb"))
        else:
            await call.message.answer("No logs yet.")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
