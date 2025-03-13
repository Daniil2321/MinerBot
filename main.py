import asyncio
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.filters.command import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Select, SwitchTo, Row, Back
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Window, setup_dialogs, Dialog, DialogManager, StartMode, ChatEvent

from states import States


BOTNAME = "имя бота"
ACCESS_TOKEN = "@Daniil_2017_228"


async def get_data(dialog_manager: DialogManager, **kwargs):
    coin = dialog_manager.dialog_data.get("coin", None)
    return {
        "coin": coin,
        "pool": dialog_manager.dialog_data.get("pool", ""),
        "wallet_address": dialog_manager.dialog_data.get("wallet_address", "")
    }


async def on_coin_changed(
    callback: ChatEvent,
    select: Any,
    dialog_manager: DialogManager,
    coin: str,
):
    dialog_manager.dialog_data["coin"] = coin
    await dialog_manager.next()


async def on_pool_changed(
    callback: ChatEvent,
    select: Any,
    dialog_manager: DialogManager,
    pool: str,
):
    dialog_manager.dialog_data["pool"] = pool
    await dialog_manager.next()


async def wallet_address_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data["wallet_address"] = message.text
    await dialog_manager.next()


async def pool_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data["pool"] = message.text
    await dialog_manager.next()


async def other_type_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    await message.answer("Text is expected")


dialog = Dialog(
    Window(
        Const(f"Привет! {BOTNAME} - это сервис для создания скрытых манеров для заработка💵!\nCreated by @Daniil_2017_228"),
        SwitchTo(Const("Начать"), id="start_button", state=States.choosing_coin),
        state=States.main
    ),
    Window(
        Const("Выбери монету"),
        Select(
            Format("{item}"),
            items=["ZEPHYR | RVN", "XMR | ETC", "XMR | RVN"],
            item_id_getter=lambda x: x,
            id="w_coin",
            on_click=on_coin_changed,
        ),
        state=States.choosing_coin,
    ),
    Window(
    Const("Введите аддресс кошелька"),
        Back(),
        MessageInput(wallet_address_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=States.sending_wallet_address
    ),
    Window(
        Const("Введите пул"),
        Back(),
        MessageInput(pool_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=States.choosing_pool,
    ),
    Window(
        Format("Вы хотте подать запрос на майнер с такими настройками:\nмонета: {coin}\nпул: {pool}\nадрдесс кошелька: {wallet_address}\nВерно?"),
        Row(
            Back(),
            SwitchTo(Const("Нет❌"), id="not_right", state=States.main),
            Button(Const("Да✅"), on_click=print("success"), id="finish"),
        ),
        getter=get_data,
        state=States.finish
    )
)


bot = Bot(token="YOUR TOKEN")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.include_routers(dialog)
setup_dialogs(dp)


async def start(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=States.main, mode=StartMode.RESET_STACK)


async def main():
    print("bot start")
    dp.message.register(start, CommandStart())
    await dp.start_polling(bot)
    print("bot end")


if __name__ == '__main__':
    asyncio.run(main())
