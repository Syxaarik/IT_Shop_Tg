import os

from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment

import app.keyboards as kb
from app.database.requests import set_user, get_items, get_items_by_category

load_dotenv()
router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    path_photo = FSInputFile('photo/blaxa.png')
    await set_user(message.from_user.id)
    caption = f'<b>Добро пожаловать</b> {message.from_user.full_name} в нашем магазине обуви.'
    await message.answer_photo(photo=path_photo, caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb.main)


@router.callback_query(F.data == 'start')
async def start_callback(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главное меню')
    await callback.message.edit_text('Добро пожаловать в наш магазин', reply_markup=kb.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите категорию товаров', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите товар по категории',
                                     reply_markup=await kb.get_items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('pay_'))
async def process_payment(callback: CallbackQuery):
    item = await get_items(callback.data.split('_')[1])

    if not item:
        await callback.answer("Ошибка: товар не найден!")
        return

    await callback.message.answer_invoice(
        title=item.name,
        description=item.description,
        payload=str(item.id),
        provider_token=os.getenv('PAY_TOKEN'),
        currency="RUB",
        prices=[LabeledPrice(label=item.name, amount=int(item.price * 100))],
        start_parameter="purchase",
        need_email=True,
        need_phone_number=True,
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == "successful_payment")
async def successful_payment_handler(message: Message):
    await message.answer("✅ Спасибо за покупку! Ваш платеж успешно обработан.")
