from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN
from states import AdRequest
from utils import get_categories, get_products_by_category

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📦 Категории товаров", "📢 Разместить рекламу"]
    keyboard.add(*buttons)
    await message.answer(
        "👋 Добро пожаловать в ЛовиХит Бот!

"
        "Выбирайте категорию или нажмите «Разместить рекламу» 👇",
        reply_markup=keyboard
    )

@dp.message_handler(Text(equals="📦 Категории товаров"))
async def show_categories(message: types.Message):
    categories = get_categories()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(cat) for cat in categories])
    await message.answer("Выберите категорию 👇", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in get_categories())
async def show_products(message: types.Message):
    products = get_products_by_category(message.text)
    for p in products:
        btns = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("📦 Посмотреть пост", url=p["Ссылка на пост в Telegram"]),
            types.InlineKeyboardButton("🛒 Купить", url=p["Ссылка на покупку (реф)"])
        )
        await message.answer(f"🔹 <b>{p['Название товара']}</b>
{p['Описание товара']}", reply_markup=btns, parse_mode="HTML")

@dp.message_handler(Text(equals="📢 Разместить рекламу"))
async def ask_name(message: types.Message):
    await message.answer("👤 Введите ваше имя:")
    await AdRequest.waiting_for_name.set()

@dp.message_handler(state=AdRequest.waiting_for_name)
async def ask_link(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🔗 Вставьте ссылку на ваш канал:")
    await AdRequest.waiting_for_link.set()

@dp.message_handler(state=AdRequest.waiting_for_link)
async def ask_comment(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("💬 Напишите комментарий:")
    await AdRequest.waiting_for_comment.set()

@dp.message_handler(state=AdRequest.waiting_for_comment)
async def send_result(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        message.from_user.id,
        f"📢 Заявка принята!

"
        f"👤 Имя: {data['name']}
"
        f"🔗 Ссылка: {data['link']}
"
        f"💬 Комментарий: {message.text}"
    )
    await state.finish()

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
