"""
Common keyboard layouts for DrAivBot
Centralized keyboard management for consistency
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💡 Анализ бизнес-идеи", callback_data="menu_analysis")],
            [InlineKeyboardButton(text="📅 Планировщик", callback_data="menu_planner")],
            [InlineKeyboardButton(text="🎯 Управление целями (в разработке)", callback_data="menu_admin")],
            [InlineKeyboardButton(text="👥 Организационная структура (в разработке)", callback_data="menu_org")],
            [InlineKeyboardButton(text="💬 Коммуникации (в разработке)", callback_data="menu_comms")],
            [InlineKeyboardButton(text="📋 Рабочие документы (в разработке)", callback_data="menu_zrs")],
            [InlineKeyboardButton(text="📚 База знаний (в разработке)", callback_data="menu_training")],
            [InlineKeyboardButton(text="⚙️ Настройки / Settings", callback_data="menu_settings")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💡 Business Idea Analysis", callback_data="menu_analysis")],
            [InlineKeyboardButton(text="📅 Planner", callback_data="menu_planner")],
            [InlineKeyboardButton(text="🎯 Goal Management (in development)", callback_data="menu_admin")],
            [InlineKeyboardButton(text="👥 Organizational Structure (in development)", callback_data="menu_org")],
            [InlineKeyboardButton(text="💬 Communications (in development)", callback_data="menu_comms")],
            [InlineKeyboardButton(text="📋 Work Documents (in development)", callback_data="menu_zrs")],
            [InlineKeyboardButton(text="📚 Knowledge Base (in development)", callback_data="menu_training")],
            [InlineKeyboardButton(text="⚙️ Настройки / Settings", callback_data="menu_settings")]
        ])


def get_back_button(lang: str = "ru") -> InlineKeyboardMarkup:
    """Get back to main menu button"""
    text = "◀️ Главное меню" if lang == "ru" else "◀️ Main Menu"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="back_to_menu")]
    ])


def get_language_selector() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="◀️ Назад / Back", callback_data="back_to_menu")]
    ])


def get_company_registration_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Get company registration menu"""
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Начать работу", callback_data="create_company")],
            [InlineKeyboardButton(text="📩 У меня есть приглашение", callback_data="have_invitation")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Get Started", callback_data="create_company")],
            [InlineKeyboardButton(text="📩 I have an invitation", callback_data="have_invitation")]
        ])


def get_cancel_button(lang: str = "ru") -> InlineKeyboardMarkup:
    """Get cancel button"""
    text = "❌ Отменить" if lang == "ru" else "❌ Cancel"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="cancel_operation")]
    ])
