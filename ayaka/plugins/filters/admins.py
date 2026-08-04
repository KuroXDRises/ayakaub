from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineQuery
from config import Config


class Admins:
    @property
    def access_list(self):
        # computed fresh every time — always reflects the current
        # Config.sudo, even if it was updated after this class was
        # instantiated (e.g. via /eval adding a new sudoer at runtime)
        return [Config.ADMIN_ID, *Config.sudo]

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
