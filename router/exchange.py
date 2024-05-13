import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from config import ADMIN_CHAT_ID, EXCHANGE_FEE_IN_PERCENT, WITHDRAWAL_FEE
from utils import payment_requests, rates

logger = logging.getLogger(__name__)

router = Router()

OPERATION = [
    "EURO2RUB",
    # 'RUB2EURO'
]
CURRENCY = ["EUR", "RUB"]


class Exchange(StatesGroup):
    operation = State()
    amount = State()
    currency = State()
    total = State()


@router.message(Command("exchange"))
async def exchange(message: Message, state: FSMContext) -> None:
    logger.info("start exchange")
    await state.set_state(Exchange.operation)

    await message.answer(
        "Hello! What's exchange operation do you want to do?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=item) for item in OPERATION]],
            resize_keyboard=True,
        ),
    )


@router.message(Exchange.operation)
async def process_operation(message: Message, state: FSMContext) -> None:
    logger.info("start choose operation")

    operation = message.text
    if operation not in OPERATION:
        await message.answer(
            "Please select a valid operation",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=item) for item in OPERATION]],
                resize_keyboard=True,
            ),
        )
        return
    await state.update_data(operation=operation)

    await state.set_state(Exchange.amount)
    await message.answer(
        "Please select the currency of which you have the precise amount to be exchanged",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=item) for item in CURRENCY]],
            resize_keyboard=True,
        ),
    )


@router.message(Exchange.amount)
async def process_entered_amount(message: Message, state: FSMContext) -> None:
    logger.info("start choose amount")

    currency = message.text
    if currency not in CURRENCY:
        await message.answer(
            "Please select a valid currency",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=item) for item in CURRENCY]],
                resize_keyboard=True,
            ),
        )
        return
    await state.update_data(currency=currency)

    await state.set_state(Exchange.total)
    await message.answer(
        "Please input the amount you want to exchange",
        resize_keyboard=True,
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Exchange.total)
async def process_total(message: Message, state: FSMContext) -> None:
    logger.info("start choose amount")
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid amount")
        return

    data = await state.get_data()
    currency = data.get("currency")
    operation = data.get("operation")

    rate = await rates(source="RUB", target="EUR")

    if currency == "RUB":
        amount_in_currency = round(
            amount * rate * (1 + EXCHANGE_FEE_IN_PERCENT / 100) + WITHDRAWAL_FEE * rate,
            0,
        )
        link = await payment_requests("EUR", amount=amount_in_currency)
        await message.answer(
            f"Commission of service: {WITHDRAWAL_FEE} \n"
            f"Conversion fee: {EXCHANGE_FEE_IN_PERCENT}% \n"
            f"Exchange rate: {round(1 / rate, 2)} \n"
            f"Link for payment: {link} \n\n"
            f"Please pay the amount of {amount_in_currency} {operation.split('2')[0]} for {operation} exchange\n"
            f"to the link above for get {amount} {currency}. \n",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif currency == "EUR":
        amount_in_currency = round(
            amount / rate * (1 - EXCHANGE_FEE_IN_PERCENT / 100) - WITHDRAWAL_FEE, 0
        )
        link = await payment_requests("EUR", amount=amount)
        await message.answer(
            f"Commission of service: {WITHDRAWAL_FEE} \n"
            f"Conversion fee: {EXCHANGE_FEE_IN_PERCENT}% \n"
            f"Exchange rate: {round(1 / rate, 2)} \n"
            f"Link for payment: {link} \n\n"
            f"Please pay the amount of {amount} {operation.split('2')[0]} for {operation} exchange\n"
            f"to the link above for get {amount_in_currency} {operation.split('2')[1]}. \n",
            reply_markup=ReplyKeyboardRemove(),
        )
    await message.bot.send_message(
        ADMIN_CHAT_ID,
        text=f"Receive a new payment request from "
        f"{message.from_user.full_name}(@{message.from_user.username}).",
    )


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


# @form_router.message(Exchange.language)
# async def process_language(message: Message, state: FSMContext) -> None:
#     data = await state.update_data(language=message.text)
#     await state.clear()
#
#     if message.text.casefold() == "python":
#         await message.reply(
#             "Python, you say? That's the language that makes my circuits light up! 😉"
#         )
#
#     await show_summary(message=message, data=data)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
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
