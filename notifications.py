"""
Notification system for DrAivBot
Sends progress updates and alerts to users
"""
from typing import Optional
from aiogram import Bot


class NotificationManager:
    """
    Manages user notifications via Telegram

    Features:
    - Task progress notifications
    - MVP preparation updates
    - Error alerts
    - System messages
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_notification(self, telegram_id: int, message: str) -> bool:
        """Send a notification to user"""
        try:
            await self.bot.send_message(chat_id=telegram_id, text=message)
            return True
        except Exception as e:
            print(f"❌ Error sending notification to {telegram_id}: {e}")
            return False

    async def notify_task_progress(
        self,
        telegram_id: int,
        task_name: str,
        status: str,
        details: Optional[str] = None
    ) -> bool:
        """
        Notify about task progress

        Args:
            telegram_id: User's Telegram ID
            task_name: Name of the task
            status: ✅ completed, 🔄 in_progress, ❌ failed
            details: Additional information
        """
        message = f"{status} {task_name}"
        if details:
            message += f"\n\n{details}"

        return await self.send_notification(telegram_id, message)

    async def notify_mvp_progress(
        self,
        telegram_id: int,
        completed_tasks: int,
        total_tasks: int,
        current_task: str
    ) -> bool:
        """
        Notify about MVP preparation progress

        Args:
            telegram_id: User's Telegram ID
            completed_tasks: Number of completed tasks
            total_tasks: Total number of tasks
            current_task: Currently executing task
        """
        progress_percent = int((completed_tasks / total_tasks) * 100)
        progress_bar = "█" * (progress_percent // 10) + "░" * (10 - progress_percent // 10)

        message = (
            f"🚀 Прогресс подготовки SaaS MVP\n\n"
            f"[{progress_bar}] {progress_percent}%\n\n"
            f"✅ Выполнено: {completed_tasks}/{total_tasks}\n"
            f"🔄 Текущая задача: {current_task}"
        )

        return await self.send_notification(telegram_id, message)

    async def notify_error(
        self,
        telegram_id: int,
        error_message: str,
        context: Optional[str] = None
    ) -> bool:
        """Notify about an error"""
        message = f"❌ Ошибка\n\n{error_message}"
        if context:
            message += f"\n\nКонтекст: {context}"

        return await self.send_notification(telegram_id, message)

    async def notify_success(
        self,
        telegram_id: int,
        success_message: str,
        details: Optional[str] = None
    ) -> bool:
        """Notify about success"""
        message = f"✅ {success_message}"
        if details:
            message += f"\n\n{details}"

        return await self.send_notification(telegram_id, message)
