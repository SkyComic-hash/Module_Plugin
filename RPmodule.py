# meta developer: @phazmalist
# meta name: RPmodule

import html
from .. import loader, utils

__version__ = (1, 1, 0)

@loader.tds
class RPmodule(loader.Module):
    """Модуль для ролевых команд by phazmalist"""

    strings = {"name": "RPmodule"}

    async def _target(self, message):
        reply = await message.get_reply_message()
        if not reply:
            return None, None, None

        target_user = await reply.get_sender()
        target_link = f'<a href="tg://user?id={target_user.id}">{getattr(target_user, "first_name", "Пользователь")}</a>'

        me = await message.client.get_me()
        me_link = f'<a href="tg://user?id={me.id}">{getattr(me, "first_name", "Я")}</a>'

        return reply, target_link, me_link

    async def _send_rp(self, message, emoji_id, action):
        reply, target, me = await self._target(message)
        if not reply:
            return await utils.answer(message, "Репли на пользователя")

        # Получаем аргументы
        args = utils.get_args_raw(message)
        addon = ""
        replica = ""

        if args:
            # Разделяем аргументы по первому переносу строки
            parts = args.split("\n", 1)
            addon = parts[0].strip()
            if len(parts) > 1:
                replica = parts[1].strip()


        emoji_html = f'<tg-emoji emoji-id="{emoji_id}">🎭</tg-emoji>'

        # Собираем схему: Эмодзи | Автор action [доп_текст] Цель
        if addon:
            text = f'{emoji_html} | {me} {action} {html.escape(addon)} {target}'
        else:
            text = f'{emoji_html} | {me} {action} {target}'

        # Если есть перенос строки — добавляем реплику снизу
        if replica:
            text += f'\n💬 С репликой: «{html.escape(replica)}»'

        await message.edit(text, parse_mode="html")

    async def выебатьcmd(self, message):
        """Принудил к интиму"""
        await self._send_rp(message, "5435938470717596379", "принудил к интиму")

    async def дать_пятьcmd(self, message):
        """Дал пять"""
        await self._send_rp(message, "5472354553527541051", "дал пять")

    async def записать_на_ноготочкиcmd(self, message):
        """Записал на ноготочки"""
        await self._send_rp(message, "5287412767840560103", "записал на ноготочки")

    async def испугатьcmd(self, message):
        """Напугал"""
        await self._send_rp(message, "5174876047635644901", "напугал")

    async def извинитьсяcmd(self, message):
        """Попросил прощения"""
        await self._send_rp(message, "5289920740978615239", "попросил прощения")

    async def изнасиловатьcmd(self, message):
        """Изнасиловал"""
        await self._send_rp(message, "5312421636555677258", "изнасиловал")

    async def кусьcmd(self, message):
        """Куснул"""
        await self._send_rp(message, "5375381278679918063", "куснул")

    async def кастрироватьcmd(self, message):
        """Кастрировал"""
        await self._send_rp(message, "5276260030557987092", "кастрировал")

    async def лизнутьcmd(self, message):
        """Лизнул"""
        await self._send_rp(message, "5462927486859890480", "лизнул")

    async def обнятьcmd(self, message):
        """Обнял"""
        await self._send_rp(message, "5289978022957440232", "обнял")

    async def отравитьcmd(self, message):
        """Отравил"""
        await self._send_rp(message, "5395547765042338606", "отравил")

    async def отдатьсяcmd(self, message):
        """Отдался"""
        await self._send_rp(message, "5296372434692234934", "отдался")

    async def поздравитьcmd(self, message):
        """Поздравил"""
        await self._send_rp(message, "5193018401810822951", "поздравил")

    async def поцеловатьcmd(self, message):
        """Поцеловал"""
        await self._send_rp(message, "5442896128758537281", "поцеловал")

    async def прижатьcmd(self, message):
        """Прижал"""
        await self._send_rp(message, "5228951455418836672", "прижал")

    async def потрогатьcmd(self, message):
        """Потрогал"""
        await self._send_rp(message, "5460841666057349535", "потрогал")

    async def пожать_рукуcmd(self, message):
        """Пожал руку"""
        await self._send_rp(message, "5796391908817244172", "пожал руку")

    async def послать_наxуйcmd(self, message):
        """Послал нахуй"""
        await self._send_rp(message, "5470028837326691625", "послал нахуй")

    async def похвалитьcmd(self, message):
        """Похвалил"""
        await self._send_rp(message, "5352761605782259896", "похвалил")

    async def понюхатьcmd(self, message):
        """Понюхал"""
        await self._send_rp(message, "5471966722275679446", "понюхал")

    async def погладитьcmd(self, message):
        """Погладил"""
        await self._send_rp(message, "5341503409872709484", "погладил")

    async def пригласить_на_чаёкcmd(self, message):
        """Позвал на чаёк"""
        await self._send_rp(message, "5875285875314661639", "позвал на чаёк")

    async def пнутьcmd(self, message):
        """Пнул"""
        await self._send_rp(message, "5372917273122054051", "пнул")

    async def покормитьcmd(self, message):
        """Накормил"""
        await self._send_rp(message, "5296565948738717418", "накормил")

    async def расстрелятьcmd(self, message):
        """Расстрелял"""
        await self._send_rp(message, "5222486447306602688", "расстрелял")

    async def сжечьcmd(self, message):
        """Спалил"""
        await self._send_rp(message, "5805344609231968562", "спалил")

    async def трахнутьcmd(self, message):
        """Трахнул"""
        await self._send_rp(message, "5472027199710192660", "трахнул")

    async def ущипнутьcmd(self, message):
        """Ущипнул"""
        await self._send_rp(message, "5472060215123778885", "ущипнул")

    async def уебатьcmd(self, message):
        """Врезал"""
        await self._send_rp(message, "5260453322548062581", "врезал")

    async def ударитьcmd(self, message):
        """Ударил"""
        await self._send_rp(message, "5472132039861871729", "ударил")

    async def убитьcmd(self, message):
        """Убил"""
        await self._send_rp(message, "5958691374244040268", "убил")

    async def шлёпнутьcmd(self, message):
        """Шлёпнул"""
        await self._send_rp(message, "5453981559608599977", "шлёпнул")

    async def шлепнутьcmd(self, message):
        """Шлёпнул"""
        await self._send_rp(message, "5453981559608599977", "шлёпнул")

    async def делать_сексcmd(self, message):
        """Сделал секс с"""
        await self._send_rp(message, "5440470756431524657", "сделал секс с")

    async def отсосатьcmd(self, message):
        """Отсосал"""
        await self._send_rp(message, "5411128690916467494", "отсосал")

    async def отлизатьcmd(self, message):
        """Отлизал"""
        await self._send_rp(message, "5830134937126180767", "отлизал")

    async def выпоротьcmd(self, message):
        """Выпорол"""
        await self._send_rp(message, "5260574612424499741", "выпорол")

    async def наказатьcmd(self, message):
        """Наказал"""
        await self._send_rp(message, "5260636717651603317", "наказал")

    async def цьомcmd(self, message):
        """Цьомнул"""
        await self._send_rp(message, "55215305764498858909", "цьомнул")

    async def поставитьcmd(self, message):
        """Поставил"""
        await self._send_rp(message, "5357041699606503565", "поставил")
