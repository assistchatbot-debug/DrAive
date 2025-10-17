"""
Company Module Handlers
Handles company registration, organizational structure display, and invitations
"""
from aiogram import types, F
from aiogram.filters import Command

from bot.modules.company import router
from bot.core.database import (
    get_user_by_telegram_id,
    create_company,
    create_user,
    get_company_positions
)
from bot.core.session import SessionManager
from bot.modules.company.orgchart import create_company_positions, format_orgchart
from bot.utils.keyboards import get_main_menu, get_company_registration_menu
from bot.utils.texts import get_text


@router.callback_query(F.data == "create_company")
async def start_company_registration(callback: types.CallbackQuery):
    """Start company registration process"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    # Update session state
    await SessionManager.update_session(
        telegram_id,
        state="COMPANY_REGISTRATION",
        data={**session.get("data", {}), "step": "company_name"}
    )

    await callback.message.answer(get_text(lang, "company_welcome"))
    await callback.answer()


@router.callback_query(F.data == "have_invitation")
async def handle_invitation_request(callback: types.CallbackQuery):
    """Handle user with invitation code"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")

    await SessionManager.update_session(
        telegram_id,
        state="AWAITING_INVITE_CODE"
    )

    if lang == "ru":
        text = "📩 Введите код приглашения или отправьте ссылку-приглашение:"
    else:
        text = "📩 Enter invitation code or send invitation link:"

    await callback.message.answer(text)
    await callback.answer()


async def process_company_name(message: types.Message):
    """Process company name input"""
    telegram_id = message.from_user.id
    session = await SessionManager.get_session(telegram_id)
    lang = session.get("data", {}).get("lang", "ru")
    company_name = message.text.strip()

    try:
        # Create company
        company = await create_company(company_name)

        # Create user
        user = await create_user(
            telegram_id=telegram_id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            company_id=company["id"],
            language=lang
        )

        # Create 21 positions
        await create_company_positions(company["id"], user["id"])

        # Update session
        await SessionManager.update_session(
            telegram_id,
            state="MENU",
            user_id=user["id"],
            company_id=company["id"]
        )

        # Success message
        success_msg = f"{get_text(lang, 'company_created')}\n\n{get_text(lang, 'company_next_steps')}"
        await message.answer(success_msg)

        # Show main menu
        await message.answer(
            f"{get_text(lang, 'menu_title')}\n{get_text(lang, 'menu_subtitle')}",
            reply_markup=get_main_menu(lang)
        )

    except Exception as e:
        error_msg = f"❌ {'Ошибка при создании компании' if lang == 'ru' else 'Error creating company'}: {str(e)}"
        await message.answer(error_msg)


@router.callback_query(F.data == "show_orgchart")
async def show_orgchart(callback: types.CallbackQuery):
    """Show organizational chart"""
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)
    company_id = session.get("company_id")
    lang = session.get("data", {}).get("lang", "ru")

    if not company_id:
        await callback.answer(get_text(lang, "error_no_company"), show_alert=True)
        return

    positions = await get_company_positions(company_id)
    text = format_orgchart(positions, lang)

    await callback.message.answer(text)
    await callback.answer()
