import os
import sys

from dotenv import load_dotenv

sys.dont_write_bytecode = True

load_dotenv()

TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID'))
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')