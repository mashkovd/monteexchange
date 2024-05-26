import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand

from config import TOKEN
from router.exchange import router
from utils import pyproject_version, rates

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

dp = Dispatcher()


@dp.message(Command("rate"))
async def echo_currency(message: Message) -> None:
    rate = await rates(source="EUR", target="RUB")
    await message.answer(f"EUR to RUB rate is {rate}")


@dp.message(Command("help"))
async def help(message: Message) -> None:
    await message.answer(
        f"If you have any questions, please contact me @mashkovd.\n\n"
        f"version of bot is {pyproject_version}"
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    logger.info(f"Hello, {html.bold(message.from_user.full_name)}!")
    # chat_id = message.chat.id
    # await message.reply(f"Your chat ID is: {chat_id}")
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!\n\n"
        f"I'm a bot that can exchange currency.\n\n"
        f"Use the following commands:\n"
        f"/exchange to start exchange process.\n"
        f"/rate to get current rate of EUR to RUB.\n"
        f"/help to get help."
    )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start the bot"),
            BotCommand(command="/exchange", description="Start the exchange process"),
            BotCommand(
                command="/rate", description="Get the current rate of EUR to RUB"
            ),
            BotCommand(command="/help", description="Get help"),
        ]
    )
    # And the run events dispatching
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
