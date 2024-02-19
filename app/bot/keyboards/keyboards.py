from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class KeyboardManager:
    back_button = types.InlineKeyboardButton(text='Назад', callback_data='back-to-main-menu')
    back_to_main_menu_button = types.InlineKeyboardButton(text='В главное меню',
                                                          callback_data='back-to-main-menu')

    @staticmethod
    def register_keyboard() -> types.ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()

        register_button = types.KeyboardButton(text="/start")

        keyboard.add(register_button)
        return keyboard.as_markup(resize_keyboard=True)

    @staticmethod
    def main_menu() -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        choose_excercise = types.InlineKeyboardButton(text='Получить список тем задач',
                                                        callback_data='get-categories')
        keyboard.add(choose_excercise)
        keyboard.adjust(1)
        return keyboard.as_markup()


    def back_to_main_menu(self) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(self.back_to_main_menu_button)
        keyboard.adjust(1)
        return keyboard.as_markup()

