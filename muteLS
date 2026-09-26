# meta developer: @phazmalist, @phazmalistPlugins
# meta name: MuteLS
# scope: hikka_only
# meta version: 1.0.0

import asyncio
import logging
import re
import time
from typing import Optional

from telethon import events
from telethon.tl.types import User, Message

from .. import loader, utils


logger = logging.getLogger(__name__)


DURATION_RE = re.compile(r"^(\d+)\s*([smhdw])$", re.IGNORECASE)

UNITS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}

DEFAULT_DURATION = "1h"


@loader.tds
class MuteLSMod(loader.Module):
    """
    Автоматически удаляет входящие сообщения
    от замьюченных пользователей в личных чатах.
    """

    strings = {
        "name": "MuteLS",

        "muted": (
            "🔇 <b>{}</b> замьючен до <b>{}</b>."
        ),

        "muted_forever": (
            "🔇 <b>{}</b> замьючен навсегда."
        ),

        "unmuted": (
            "🔊 <b>{}</b> размьючен."
        ),

        "not_muted": (
            "ℹ️ Этот пользователь не находится в муте."
        ),

        "already_muted": (
            "ℹ️ Этот пользователь уже находится в муте."
        ),

        "private_only": (
            "⚠️ Эта команда работает только в личном чате."
        ),

        "invalid_duration": (
            "⚠️ Неверный формат времени.\n\n"
            "Примеры: <code>30m</code>, <code>2h</code>, "
            "<code>1d</code>, <code>1w</code>."
        ),

        "status_muted": (
            "🔇 <b>{}</b> находится в муте до <b>{}</b>."
        ),

        "status_forever": (
            "🔇 <b>{}</b> находится в муте навсегда."
        ),

        "status_empty": (
            "🔊 Этот пользователь не находится в муте."
        ),

        "no_mutes": (
            "🔊 Нет замьюченных пользователей."
        ),

        "mutes_header": (
            "🔇 <b>Замьюченные пользователи:</b>\n\n{}"
        ),

        "error": (
            "❌ Ошибка: <code>{}</code>"
        ),

        "deleted": (
            "🗑 Удалено сообщений: <b>{}</b>"
        ),

        "cfg_default_duration": (
            "Длительность мута по умолчанию"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "DEFAULT_DURATION",
                DEFAULT_DURATION,
                doc=lambda: self.strings("cfg_default_duration"),
                validator=loader.validators.String(),
            ),
        )

        self.muted = {}
        self._handler = None

    # ============================================================
    # ИНИЦИАЛИЗАЦИЯ
    # ============================================================

    async def client_ready(self, client, db):
        """
        Инициализация модуля.
        """

        self._client = client
        self._db = db

        self.muted = self._db.get(
            self.strings["name"],
            "muted",
            {}
        )

        if not isinstance(self.muted, dict):
            self.muted = {}

        self._remove_expired()

        # Обработчик входящих сообщений
        self._handler = client.add_event_handler(
            self._incoming_message,
            events.NewMessage(incoming=True)
        )

        logger.info(
            "[MuteLS] Module loaded. Muted users: %s",
            len(self.muted)
        )

    # ============================================================
    # СОХРАНЕНИЕ
    # ============================================================

    def _save(self):
        """
        Сохраняет список мутов в Hikka DB.
        """

        self._db.set(
            self.strings["name"],
            "muted",
            self.muted
        )

    # ============================================================
    # РАБОТА С ДЛИТЕЛЬНОСТЬЮ
    # ============================================================

    def _parse_duration(self, text: str) -> Optional[int]:
        """
        Преобразует:
            30m
            2h
            1d
            1w

        в секунды.
        """

        if not text:
            return None

        match = DURATION_RE.match(text.strip())

        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2).lower()

        if value <= 0:
            return None

        return value * UNITS[unit]

    def _format_until(self, timestamp: int) -> str:
        """
        Форматирует время окончания мута.
        """

        remaining = timestamp - int(time.time())

        if remaining <= 0:
            return "истёк"

        days, remaining = divmod(remaining, 86400)
        hours, remaining = divmod(remaining, 3600)
        minutes, seconds = divmod(remaining, 60)

        parts = []

        if days:
            parts.append(f"{days}д")

        if hours:
            parts.append(f"{hours}ч")

        if minutes:
            parts.append(f"{minutes}м")

        if not parts and seconds:
            parts.append(f"{seconds}с")

        return " ".join(parts)

    # ============================================================
    # МУТЫ
    # ============================================================

    def _remove_expired(self):
        """
        Удаляет просроченные временные муты.
        """

        now = int(time.time())
        changed = False

        for user_id in list(self.muted.keys()):
            try:
                entry = self.muted[user_id]

                until = int(entry.get("until", 0))

                if until and until <= now:
                    del self.muted[user_id]
                    changed = True

            except Exception:
                del self.muted[user_id]
                changed = True

        if changed:
            self._save()

    def _is_muted(self, user_id: int) -> bool:
        """
        Проверяет, находится ли пользователь в муте.
        """

        self._remove_expired()

        return str(user_id) in self.muted

    async def _get_user_name(self, user_id: int) -> str:
        """
        Получает отображаемое имя пользователя.
        """

        try:
            entity = await self._client.get_entity(user_id)

            first_name = getattr(entity, "first_name", None) or ""
            last_name = getattr(entity, "last_name", None) or ""

            name = f"{first_name} {last_name}".strip()

            if name:
                return name

            username = getattr(entity, "username", None)

            if username:
                return f"@{username}"

        except Exception:
            pass

        return f"id {user_id}"

    # ============================================================
    # ВХОДЯЩИЕ СООБЩЕНИЯ
    # ============================================================

    async def _incoming_message(self, event):
        """
        Главная логика оригинального модуля.

        Если сообщение:
        - входящее;
        - находится в личном чате;
        - отправитель замьючен;

        оно удаляется.
        """

        try:
            if not event.is_private:
                return

            message = event.message

            if not message:
                return

            # Сообщения без отправителя пропускаем
            sender = await event.get_sender()

            if not sender:
                return

            # Нужен именно пользователь
            if not isinstance(sender, User):
                return

            user_id = int(sender.id)

            if not self._is_muted(user_id):
                return

            # Удаляем входящее сообщение
            await self._client.delete_messages(
                entity=event.chat_id,
                message_ids=[message.id],
                revoke=True
            )

            logger.debug(
                "[MuteLS] Deleted message %s from %s",
                message.id,
                user_id
            )

        except Exception as e:
            logger.exception(
                "[MuteLS] Incoming message handler error: %s",
                e
            )

    # ============================================================
    # .mute
    # ============================================================

    @loader.command(
        ru_doc="Замьютить пользователя в текущем личном чате"
    )
    async def mute(self, message: Message):
        """
        .mute
        .mute 30m
        .mute 2h
        .mute 1d
        .mute 1w
        """

        try:
            if not message.is_private:
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            sender = await message.get_chat()

            if not isinstance(sender, User):
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            user_id = int(sender.id)

            # Нельзя замьютить самого себя
            me = await self._client.get_me()

            if user_id == int(me.id):
                await utils.answer(
                    message,
                    "⚠️ Нельзя замьютить самого себя."
                )
                return

            self._remove_expired()

            user_key = str(user_id)

            if user_key in self.muted:
                await utils.answer(
                    message,
                    self.strings["already_muted"]
                )
                return

            args = utils.get_args_raw(message).strip()

            if not args:
                args = self.config["DEFAULT_DURATION"].strip()

            until = 0

            # Пустое значение = навсегда
            if args:
                seconds = self._parse_duration(args)

                if seconds is None:
                    await utils.answer(
                        message,
                        self.strings["invalid_duration"]
                    )
                    return

                until = int(time.time()) + seconds

            name = await self._get_user_name(user_id)

            self.muted[user_key] = {
                "id": user_id,
                "name": name,
                "until": until,
            }

            self._save()

            if until:
                await utils.answer(
                    message,
                    self.strings["muted"].format(
                        name,
                        self._format_until(until)
                    )
                )
            else:
                await utils.answer(
                    message,
                    self.strings["muted_forever"].format(
                        name
                    )
                )

        except Exception as e:
            logger.exception("[MuteLS] mute error")

            await utils.answer(
                message,
                self.strings["error"].format(
                    str(e)
                )
            )

    # ============================================================
    # .unmute
    # ============================================================

    @loader.command(
        ru_doc="Снять мут с пользователя в текущем личном чате"
    )
    async def unmute(self, message: Message):
        """
        .unmute
        """

        try:
            if not message.is_private:
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            sender = await message.get_chat()

            if not isinstance(sender, User):
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            user_id = int(sender.id)
            user_key = str(user_id)

            self._remove_expired()

            entry = self.muted.pop(user_key, None)

            if entry is None:
                await utils.answer(
                    message,
                    self.strings["not_muted"]
                )
                return

            self._save()

            name = entry.get("name") or f"id {user_id}"

            await utils.answer(
                message,
                self.strings["unmuted"].format(name)
            )

        except Exception as e:
            logger.exception("[MuteLS] unmute error")

            await utils.answer(
                message,
                self.strings["error"].format(
                    str(e)
                )
            )

    # ============================================================
    # .mutestatus
    # ============================================================

    @loader.command(
        ru_doc="Показать статус мута текущего пользователя"
    )
    async def mutestatus(self, message: Message):
        """
        .mutestatus
        """

        try:
            if not message.is_private:
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            sender = await message.get_chat()

            if not isinstance(sender, User):
                await utils.answer(
                    message,
                    self.strings["private_only"]
                )
                return

            user_id = int(sender.id)

            self._remove_expired()

            entry = self.muted.get(str(user_id))

            if entry is None:
                await utils.answer(
                    message,
                    self.strings["status_empty"]
                )
                return

            name = entry.get("name") or f"id {user_id}"
            until = int(entry.get("until", 0) or 0)

            if until:
                await utils.answer(
                    message,
                    self.strings["status_muted"].format(
                        name,
                        self._format_until(until)
                    )
                )
            else:
                await utils.answer(
                    message,
                    self.strings["status_forever"].format(
                        name
                    )
                )

        except Exception as e:
            logger.exception("[MuteLS] mutestatus error")

            await utils.answer(
                message,
                self.strings["error"].format(
                    str(e)
                )
            )

    # ============================================================
    # .mutes
    # ============================================================

    @loader.command(
        ru_doc="Показать список замьюченных пользователей"
    )
    async def mutes(self, message: Message):
        """
        .mutes
        """

        try:
            self._remove_expired()

            if not self.muted:
                await utils.answer(
                    message,
                    self.strings["no_mutes"]
                )
                return

            lines = []

            for user_key, entry in self.muted.items():

                user_id = entry.get("id", user_key)
                name = entry.get("name") or f"id {user_id}"
                until = int(entry.get("until", 0) or 0)

                if until:
                    duration = self._format_until(until)
                    lines.append(
                        f"🔇 <b>{name}</b> — {duration}"
                    )
                else:
                    lines.append(
                        f"🔇 <b>{name}</b> — навсегда"
                    )

            await utils.answer(
                message,
                self.strings["mutes_header"].format(
                    "\n".join(lines)
                )
            )

        except Exception as e:
            logger.exception("[MuteLS] mutes error")

            await utils.answer(
                message,
                self.strings["error"].format(
                    str(e)
                )
            )

    # ============================================================
    # .mutehelp
    # ============================================================

    @loader.command(
        ru_doc="Показать справку MuteLS"
    )
    async def mutehelp(self, message: Message):
        """
        .mutehelp
        """

        text = (
            "🔇 <b>MuteLS</b>\n\n"
            "<code>.mute</code> — мут на стандартное время\n"
            "<code>.mute 30m</code> — мут на 30 минут\n"
            "<code>.mute 2h</code> — мут на 2 часа\n"
            "<code>.mute 1d</code> — мут на 1 день\n"
            "<code>.mute 1w</code> — мут на 1 неделю\n\n"
            "<code>.unmute</code> — снять мут\n"
            "<code>.mutestatus</code> — статус текущего чата\n"
            "<code>.mutes</code> — список мутов\n"
            "<code>.mutehelp</code> — эта справка\n\n"
            "📌 Работает только с личными чатами.\n"
            "📌 Входящие сообщения замьюченных пользователей "
            "автоматически удаляются."
        )

        await utils.answer(message, text)

    # ============================================================
    # ВЫГРУЗКА
    # ============================================================

    async def on_unload(self):
        """
        Отключение обработчика при выгрузке модуля.
        """

        try:
            if self._handler is not None:
                self._client.remove_event_handler(
                    self._handler,
                    events.NewMessage(incoming=True)
                )

                self._handler = None

        except Exception as e:
            logger.exception(
                "[MuteLS] unload error: %s",
                e
            )
