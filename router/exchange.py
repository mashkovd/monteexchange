from aiogram import Router
from aiogram.types import ForceReply
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import F, html
from typing import Any
import logging
from utils import payment_requests, rates
from config import WITHDRAWAL_FEE, EXCHANGE_FEE_IN_PERCENT

logger = logging.getLogger(__name__)

form_router = Router()

OPERATION = ['EURO2RUB', 'RUB2EURO']
CURRENCY = ['EUR']
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='30_000'),
        KeyboardButton(text='50_000'),
        KeyboardButton(text='60_000'),
    ]
], )


async def show_summary(message: Message, data: dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


class Form(StatesGroup):
    currency = State()
    source_amount = State()
    target_amount = State()
    language = State()


@form_router.message(Command("exchange"))
async def exchange(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.currency)
    logger.info("start exchange")

    await message.answer(
        "Hello! What's currency you want to exchange? Only EUR is available for now.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=item) for item in CURRENCY]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.currency)
async def process_amount(message: Message, state: FSMContext) -> None:
    currency = message.text
    await state.update_data(action=currency)
    if currency not in CURRENCY:
        await message.answer("Please select a valid currency", resize_keyboard=True)
        return
    await state.set_state(Form.source_amount)
    await message.answer("Please enter or choose on keyboard an amount rubles you need to get",
                         reply_markup=keyboard, resize_keyboard=True)


# @form_router.message(Form.source_amount)
# async def process_amount(message: Message, state: FSMContext) -> None:
#     action = await state.update_data(action=message.text)
#     await state.set_state(Form.source_amount)
#     if action == 'EURO2RUB':
#         rate = await rates(source='EUR', target='RUB')
#     await message.answer("Please enter an amount from 100 to 1000",
#                          reply_markup=keyboard, action=action)

@form_router.message(Form.source_amount)
async def process_entered_amount(message: Message) -> None:
    try:
        source_amount = int(message.text)
        if 10_000 <= source_amount <= 200_000:
            rate = await rates(source='RUB', target='EUR')
            amount = round(source_amount * rate * (1 + EXCHANGE_FEE_IN_PERCENT / 100)
                           + WITHDRAWAL_FEE, 0)
            # The amount is valid, you can proceed with your logic here
            link = await payment_requests("EUR", amount=amount)
            await message.answer(f"Commission of service: {WITHDRAWAL_FEE} \n"
                                 f"Conversion fee: {EXCHANGE_FEE_IN_PERCENT}% \n"
                                 f"Exchange rate: {rate} \n"
                                 f"Link for payment: {link}")
            await message.bot.send_message(210408407,
                                           text=f"Receive a new payment request from "
                                                f"{message.from_user.full_name}(@{message.from_user.username}).")

        else:
            await message.reply("Please enter a valid amount between 10_000 and 200_000.", reply_markup=ForceReply())
    except ValueError:
        await message.reply("Please enter a valid integer.", reply_markup=ForceReply())
    # await state.set_state(Form.like_bots)
    # await message.answer(
    #     f"Nice to meet you, {html.quote(message.text)}!\nDid you like to write bots?",
    #     reply_markup=ReplyKeyboardMarkup(
    #         keyboard=[
    #             [
    #                 KeyboardButton(text="Yes"),
    #                 KeyboardButton(text="No"),
    #             ]
    #         ],
    #         resize_keyboard=True,
    #     ),
    # )


# @form_router.message(Form.like_bots, F.text.casefold() == "no")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     await state.clear()
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await show_summary(message=message, data=data, positive=False)
#
#
# @form_router.message(Form.like_bots, F.text.casefold() == "yes")
# async def process_like_write_bots(message: Message, state: FSMContext) -> None:
#     await state.set_state(Form.language)
#
#     await message.reply(
#         "Cool! I'm too!\nWhat programming language did you use for it?",
#         reply_markup=ReplyKeyboardRemove(),
#     )


@form_router.message(Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)
    await state.clear()

    if message.text.casefold() == "python":
        await message.reply(
            "Python, you say? That's the language that makes my circuits light up! 😉"
        )

    await show_summary(message=message, data=data)


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )
