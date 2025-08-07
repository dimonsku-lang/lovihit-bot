from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, GOOGLE_SHEET_URL
from utils import get_categories, get_products_by_category, send_ad_request

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📦 Категории товаров", "🔥 Подборки недели", "📢 Разместить рекламу"]
    keyboard.add(*buttons)
    await message.answer(
        "👋 Добро пожаловать в ЛовиХит Бот!

"
        "Выбирайте категорию или подборку, а если хотите рекламу — нажмите соответствующую кнопку 👇",
        reply_markup=keyboard
    )

@dp.message_handler(lambda msg: msg.text == "📦 Категории товаров")
async def show_categories(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = get_categories()
    keyboard.add(*[types.KeyboardButton(cat) for cat in categories])
    await message.answer("Выберите категорию 👇", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in get_categories())
async def show_products(message: types.Message):
    products = get_products_by_category(message.text)
    for product in products:
        btns = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("📦 Посмотреть пост", url=product["post_url"]),
            types.InlineKeyboardButton("🛒 Купить", url=product["buy_url"])
        )
        await message.answer(f"🔹 <b>{product['name']}</b>
{product['desc']}", reply_markup=btns, parse_mode="HTML")

@dp.message_handler(lambda msg: msg.text == "📢 Разместить рекламу")
async def ad_request(message: types.Message):
    await send_ad_request(message, bot)

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
