from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    main = State()
    choosing_coin = State()
    choosing_pool = State()
    sending_wallet_address = State()
    finish = State()
