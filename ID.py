# meta developer: @phazmalist, @phazmalistPlugins
# meta banner: https://raw.githubusercontent.com/SkyComic-hash/Banner/main/ID.jpg
# meta name: ID
# scope: hikka_only
# meta version: 1.0.0

__version__ = (1, 0, 0)

from .. import loader, utils
import telethon as tl

@loader.tds
class ID(loader.Module):
    """ID of all!"""

    strings = {
    "name": "ID",
    "Error_reply": "<emoji document_id=5328145443106873128>✖️</emoji> <b>Where your reply?</b>",
    "not_chat": "<emoji document_id=5328145443106873128>✖️</emoji> <b>This is not a chat!</b>"
    }

    strings_ru = {
    "Error_reply": "<emoji document_id=5328145443106873128>✖️</emoji> <b>Где твой реплай?</b>",
    "not_chat": "<emoji document_id=5328145443106873128>✖️</emoji> <b>Это не чат!</b>"
}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "bot_api_id",
                "True",
                "Bot API id for channels and chats",
                validator=loader.validators.Boolean(),
            ),
        )

    
    async def useridcmd(self, message):
        """[reply or username] | Get User ID"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            if args:
                user = await message.client.get_entity(
                    args if not args.isdigit() else int(args)
                )
            else:
                user = await message.client.get_entity(reply.sender_id)
        except ValueError:
            user = await message.client.get_entity(message.sender_id)

        if isinstance(user, tl.types.User):
            await utils.answer(message, f"<emoji document_id=5287702390370242449>🌙</emoji> <bUser:</b> <code>{user.first_name}</code>\n<emoji document_id=5287702390370242449>🌙</emoji> <b>User ID:</b> <code>{user.id}</code>")

        elif self.config["bot_api_id"] == True:
            await utils.answer(message, f"<emoji document_id=5287702390370242449>🌙</emoji> <bUser:</b> <code>{user.title}</code>\n<emoji document_id=5287702390370242449>🌙</emoji> <b>User ID:</b> <code>-100{user.id}</code>")

        else:
            await utils.answer(message, f"<emoji document_id=5287702390370242449>🌙</emoji> <bUser:</b> <code>{user.title}</code>\n<emoji document_id=5287702390370242449>🌙</emoji> <b>User ID:</b> <code>{user.id}</code>")

    async def idcmd(self, message):
        """| Get your & user/bot/chat ID"""

        me = await message.client.get_me()
        lines = [f"<emoji document_id=5287702390370242449>🌙</emoji> <b>Мой ID:</b> <code>{me.id}</code>"]

        if message.is_private:
            chat = await message.get_chat()

            if isinstance(chat, tl.types.User) and chat.bot:
                lines = [
                    f"<emoji document_id=5287702390370242449>🌙</emoji> <b>ID бота:</b> <code>{chat.id}</code>",
                    f"<emoji document_id=5287702390370242449>🌙</emoji> <b>Мой ID:</b> <code>{me.id}</code>",
                ]
            elif chat.id != me.id:
                lines.append(f"<emoji document_id=5287702390370242449>🌙</emoji> <b>ID собеседника:</b> <code>{chat.id}</code>")
        else:
            chat_id = message.chat_id if self.config["bot_api_id"] == True else (await message.get_chat()).id
            lines.append(f"<emoji document_id=5287702390370242449>🌙</emoji> <b>ID чата:</b> <code>{chat_id}</code>")

        await utils.answer(message, "\n".join(lines))

    async def chatidcmd(self, message):
        """| Get chat ID"""

        if message.is_private:
            await utils.answer(message, self.strings("not_chat", message))
            return

        chat = await message.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "first_name", "Chat")

        chat_id = message.chat_id if self.config["bot_api_id"] == True else chat.id

        await utils.answer(message, f"<emoji document_id=5287702390370242449>🌙</emoji><code> {title}</code>\n<emoji document_id=5287702390370242449>🌙</emoji> <b>Chat ID</b>: <code>{chat_id}</code>")
