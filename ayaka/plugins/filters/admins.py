from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineQuery
from config import Config


class Admins:
    def __init__(self):
        self.access_list = [Config.ADMIN_ID, *Config.sudo]
        
    def message(self):
        def func(_, __, m: Message):
            return m.from_user.id in self.access_list
        return filters.create(func, name="IsAdminMessage")

    def callback(self):
        def func(_, __, q: CallbackQuery):
            return q.from_user.id in self.access_list
        return filters.create(func, name="IsAdminCallback")

    def inline(self):
        def func(_, __, q: InlineQuery):
            return q.from_user.id in self.access_list
        return filters.create(func, name="IsAdminInline")

ADMINS = Admins()