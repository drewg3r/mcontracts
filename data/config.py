from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

MIN_RID = env.int("MIN_RID")
MAX_RID = env.int("MAX_RID")