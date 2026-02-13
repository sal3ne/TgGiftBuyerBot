from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError

from app.core.config import settings
from app.core.logger import logger
from app.infrastructure.db.database import init_db, close_db
from app.infrastructure.scheduler.jobs import schedule_sync_job
from app.interfaces.telegram.handlers import register_handlers
from app.interfaces.telegram.middlewares.private_chat_only import (
    PrivateChatOnlyMiddleware,
)
from app.interfaces.telegram.middlewares.error_handler import (
    ErrorHandlerMiddleware,
)
from app.interfaces.telegram.middlewares.back_button_middleware import (
    BackButtonMiddleware,
)

bot = Bot(
    token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

dp.message.middleware(PrivateChatOnlyMiddleware())
dp.callback_query.middleware(PrivateChatOnlyMiddleware())
dp.message.middleware(ErrorHandlerMiddleware())
dp.callback_query.middleware(ErrorHandlerMiddleware())
dp.message.middleware(BackButtonMiddleware())


@dp.errors()
async def errors_handler(update, exception):
    if isinstance(exception, TelegramForbiddenError):
        logger.warning(f"Bot was blocked by user: {exception}")
        return
    logger.error(f"Unhandled exception: {exception}")


@logger.catch
async def on_startup():
    logger.info("Initializing database...")
    await init_db()  # Используем async версию
    logger.info("Database initialized successfully")

    logger.info("Starting scheduler...")
    schedule_sync_job(bot)


@logger.catch
async def main():
    logger.info("Starting bot...")

    await on_startup()

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await close_db()