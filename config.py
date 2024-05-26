from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")
WISE_HOST = env.str("WISE_HOST")
WISE_TOKEN = env.str("WISE_TOKEN")

PROFILE_ID = env.int("PROFILE_ID", 27614777)
BALANCE_ID = env.int("BALANCE_ID", 28951646)
REFERRAL_LINK = env.str("REFERRAL_LINK", "https://wise.com/invite/dic/dmitriim215")

WITHDRAWAL_FEE_IN_EURO = env.int("WITHDRAWAL_FEE", 5)
EXCHANGE_FEE_IN_PERCENT = env.float("EXCHANGE_FEE_IN_PERCENT", 2.5)

ADMIN_CHAT_ID = env.int("ADMIN_BOT_ID", 210408407)
