from pathlib import Path

from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

MIN_RID = env.int("MIN_RID")
MAX_RID = env.int("MAX_RID")

I18N_DOMAIN = "bot-loc"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'data' / 'locales'
