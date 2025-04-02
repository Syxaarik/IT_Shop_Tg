import asyncio
import os
from app.database.models import async_main
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher(scip_updates=False)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

