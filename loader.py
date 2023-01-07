import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from jinja2 import FileSystemLoader, Environment
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ADMINS = os.getenv('ADMINS')

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)