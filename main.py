"""
DrAivBot - AI-powered Business Strategy Advisor
Modular, scalable Telegram bot for enterprise SaaS management

Architecture:
- Core: Database, Session Management, Notifications
- Modules: Analysis, Planner, Company, Admin Scale, Communications, ZRS, Training
- Utils: Keyboards, Texts (i18n)

Version: 2.0.0 (Modular Architecture)
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BotCommand

from bot.config import BOT_TOKEN, REDIS_URL, ENABLE_REDIS_CACHE
# Temporary: Using simple in-memory sessions instead of database
# from bot.core.database import get_user_by_telegram_id
from bot.core.simple_session import SimpleSessionManager as SessionManager
from bot.core.notifications import NotificationManager
from bot.core.redis_cache import init_redis_cache, close_redis_cache

# Mock function for get_user_by_telegram_id
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user lookup - returns None (user not found)"""
    return None
from bot.utils.keyboards import get_main_menu, get_company_registration_menu, get_language_selector
from bot.utils.texts import get_text

# Import module routers
from bot.modules.company import router as company_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Register module routers
dp.include_router(company_router)

# Initialize notification manager
notifications = NotificationManager(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    telegram_id = message.from_user.id

    # Initialize or get session
    session = await SessionManager.get_session(telegram_id)

    # Detect user language
    user_lang = message.from_user.language_code or "ru"
    if user_lang not in ["ru", "en"]:
        user_lang = "ru"

    # Update session with language
    data = session.get("data", {})
    data["lang"] = user_lang
    await SessionManager.update_session(telegram_id, data=data)

    # Check if user has invitation code in /start
    args = message.text.split(maxsplit=1)
    if len(args) > 1 and args[1].startswith("invite_"):
        # Handle invitation flow
        invite_code = args[1]
        # TODO: Implement invitation acceptance
        await message.answer("📩 Processing invitation...")
        return

    # Check if user exists in database
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        # User already registered
        await SessionManager.update_session(
            telegram_id,
            user_id=user["id"],
            company_id=user["company_id"],
            state="MENU"
        )

        await message.answer(
            f"{get_text(user_lang, 'welcome')}\n\n{get_text(user_lang, 'menu_title')}\n{get_text(user_lang, 'menu_subtitle')}",
            reply_markup=get_main_menu(user_lang)
        )
    else:
        # New user - needs to register company
        await message.answer(
            f"{get_text(user_lang, 'welcome')}\n\n{get_text(user_lang, 'intro')}\n\n👇 {'Выберите действие:' if user_lang == 'ru' else 'Choose an option:'}",
            reply_markup=get_company_registration_menu(user_lang)
        )


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Show main menu"""
    telegram_id = message.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    await message.answer(
        f"{get_text(lang, 'menu_title')}\n{get_text(lang, 'menu_subtitle')}",
        reply_markup=get_main_menu(lang)
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Return to main menu"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    await SessionManager.update_session(telegram_id, state="MENU")

    await callback.message.answer(
        f"{get_text(lang, 'menu_title')}\n{get_text(lang, 'menu_subtitle')}",
        reply_markup=get_main_menu(lang)
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_settings")
async def menu_settings(callback: types.CallbackQuery):
    """Show settings menu"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    await callback.message.answer(
        get_text(lang, "choose_lang"),
        reply_markup=get_language_selector()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("lang_"))
async def change_language(callback: types.CallbackQuery):
    """Change user language"""
    telegram_id = callback.from_user.id
    new_lang = callback.data.split("_")[1]

    session = await SessionManager.get_session(telegram_id)
    data = session.get("data", {})
    data["lang"] = new_lang

    await SessionManager.update_session(telegram_id, data=data)

    await callback.message.answer(
        f"{get_text(new_lang, 'lang_set')}: {'🇷🇺 Русский' if new_lang == 'ru' else '🇬🇧 English'}"
    )
    await callback.message.answer(
        f"{get_text(new_lang, 'menu_title')}\n{get_text(new_lang, 'menu_subtitle')}",
        reply_markup=get_main_menu(new_lang)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("menu_"))
async def menu_sections(callback: types.CallbackQuery):
    """Handle menu section callbacks"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    section = callback.data.replace("menu_", "")

    # Sections in development
    if section in ["admin", "org", "comms", "zrs", "training", "analysis", "planner"]:
        from bot.utils.keyboards import get_back_button

        await callback.message.answer(
            f"{get_text(lang, 'under_dev')}\n<b>{section.upper()}</b>",
            reply_markup=get_back_button(lang)
        )
    await callback.answer()


@dp.message()
async def handle_message(message: types.Message):
    """Handle text messages based on current state"""
    telegram_id = message.from_user.id
    session = await SessionManager.get_session(telegram_id)
    state = session.get("state", "MENU")

    # Company registration flow
    if state == "COMPANY_REGISTRATION":
        from bot.modules.company.handlers import process_company_name
        await process_company_name(message)
        return

    # Default: redirect to menu
    lang = session.get("data", {}).get("lang", "ru")
    await message.answer(
        f"{get_text(lang, 'menu_title')}\n{get_text(lang, 'menu_subtitle')}",
        reply_markup=get_main_menu(lang)
    )


async def set_bot_commands():
    """Set bot commands in Telegram menu"""
    commands_ru = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="menu", description="📋 Показать меню"),
    ]

    commands_en = [
        BotCommand(command="start", description="🏠 Main Menu"),
        BotCommand(command="menu", description="📋 Show Menu"),
    ]

    await bot.set_my_commands(commands_ru, language_code="ru")
    await bot.set_my_commands(commands_en, language_code="en")
    await bot.set_my_commands(commands_ru)

    logger.info("✅ Bot commands configured (RU/EN)")


async def cleanup_sessions():
    """Periodically clean up expired sessions"""
    while True:
        try:
            deleted_count = await SessionManager.cleanup_expired_sessions()
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired sessions")
        except Exception as e:
            logger.error(f"❌ Error cleaning sessions: {e}")

        # Run every hour
        await asyncio.sleep(3600)


async def main():
    """Main entry point"""
    logger.info("🚀 Starting DrAivBot v2.0 (Modular Architecture)")

    # Initialize Redis cache (optional)
    if ENABLE_REDIS_CACHE and REDIS_URL:
        redis_cache = await init_redis_cache(REDIS_URL)
        if redis_cache:
            logger.info("✅ Redis cache enabled")
        else:
            logger.warning("⚠️ Redis unavailable, using Supabase only")
    else:
        logger.info("ℹ️ Redis cache disabled")
        await init_redis_cache(None)

    # Set bot commands
    await set_bot_commands()

    # Start background tasks
    asyncio.create_task(cleanup_sessions())

    try:
        # Start polling
        logger.info("✅ Bot started successfully")
        await dp.start_polling(bot)
    finally:
        # Cleanup on shutdown
        await close_redis_cache()
        logger.info("👋 Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
