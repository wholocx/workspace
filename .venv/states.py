from aiogram.fsm.state import State, StatesGroup


class FSMSettings(StatesGroup):

    # set user location
    set_location = State()

