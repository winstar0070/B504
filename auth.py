from __future__ import annotations

from typing import Callable, Optional

from telegram import Update
from telegram.ext import ContextTypes

from bot_config import BotConfig


def get_user_id(update: Update) -> Optional[int]:
    user = update.effective_user
    return user.id if user else None


def is_admin(cfg: BotConfig, user_id: Optional[int]) -> bool:
    return bool(user_id) and int(user_id) in cfg.admins


def has_area_access(cfg: BotConfig, user_id: Optional[int], area: str) -> bool:
    if is_admin(cfg, user_id):
        return True
    return bool(user_id) and int(user_id) in cfg.users_for_area(area)


def is_command_allowed(cfg: BotConfig, user_id: Optional[int], area: str, command: str) -> bool:
    if is_admin(cfg, user_id):
        return True
    allowed = cfg.commands_for_area(area)
    return command in allowed


def guard(area_arg_index: int, command_name: str) -> Callable:
    """Decorator for PTB async handlers to enforce area + command access.

    - area_arg_index: index in context.args where area name is expected
    - command_name: command identifier used in config matching
    """

    def decorator(func: Callable):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            cfg: BotConfig = context.bot_data.get("config")  # injected in main
            uid = get_user_id(update)

            # Resolve area from args
            args = context.args or []
            if len(args) <= area_arg_index:
                await update.effective_message.reply_text("사용 형식: /%s <area>" % command_name)
                return
            area = args[area_arg_index].lower()

            if not has_area_access(cfg, uid, area):
                await update.effective_message.reply_text("이 영역에 대한 접근 권한이 없습니다.")
                return

            if not is_command_allowed(cfg, uid, area, command_name):
                await update.effective_message.reply_text("이 명령은 해당 영역에서 허용되지 않습니다.")
                return

            return await func(update, context)

        return wrapper

    return decorator
