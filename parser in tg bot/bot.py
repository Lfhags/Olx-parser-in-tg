import asyncio
import logging
import sys
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramConflictError
from app.database.models import async_main


project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

from config import TOKEN
from app.handlers import router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except TelegramConflictError:
        logging.error("Another instance of the bot is already running. Please stop other instances and try again.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")