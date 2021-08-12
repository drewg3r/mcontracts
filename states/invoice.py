from aiogram.dispatcher.filters.state import StatesGroup, State


class NewInvoiceStates(StatesGroup):
    enter_receiver = State()
    enter_sum = State()
    enter_description = State()
    done = State()
