from config import GOOGLE_SHEET_URL
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_gsheet():
    # Заглушка для примера — здесь должен быть код подключения к Google Sheets
    return []

def get_categories():
    return ["🏡 Дом и быт", "👗 Одежда и обувь", "📱 Техника и гаджеты", "🍽 Кухня", "🎁 Подарки и лайфхаки", "🚗 Авто"]

def get_products_by_category(category):
    # Заглушка — пример 2 товаров
    return [
        {
            "name": "Складная полка",
            "desc": "Идеально для ванной",
            "post_url": "https://t.me/lovihit/123",
            "buy_url": "https://wildberries.ru/..."
        },
        {
            "name": "Летний костюм",
            "desc": "Мягкий и удобный",
            "post_url": "https://t.me/lovihit/124",
            "buy_url": "https://ozon.ru/..."
        }
    ]

async def send_ad_request(message, bot):
    await message.answer("👤 Введите ваше имя:")
    name = await bot.wait_for('message')
    await message.answer("🔗 Вставьте ссылку на ваш канал:")
    channel = await bot.wait_for('message')
    await message.answer("💬 Напишите комментарий:")
    comment = await bot.wait_for('message')
    admin_id = message.from_user.id
    await bot.send_message(admin_id, f"📢 Новая заявка:
Имя: {name.text}
Ссылка: {channel.text}
Комментарий: {comment.text}")
