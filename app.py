import asyncio
from aiogram import Bot, Dispatcher
from decouple import config
from handlers.user_handler import user_router
from handlers.task_handler import task_router


TOKEN = config("TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(task_router)
dp.include_router(user_router)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
