import logging
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

from loader import dp
import handlers


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
