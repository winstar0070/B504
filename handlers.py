from __future__ import annotations

from typing import Final, Optional

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from auth import guard, get_user_id
from bot_config import BotConfig
from providers import tuya, lg_thinq, smartthings, others

WELCOME_TEXT: Final[str] = (
    "안녕하세요! 👋\n\n"
    "기본 텔레그램 봇 템플릿입니다.\n"
    "사용 가능한 명령어는 /help 로 확인하세요."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user else "사용자"
    await update.message.reply_text(f"{name}님, 환영합니다!\n\n{WELCOME_TEXT}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "사용 가능한 명령어:\n"
        "- /start — 시작 안내\n"
        "- /help — 도움말 보기\n"
        "- /areas — 접근 가능한 영역 조회\n"
        "- /whoami — 내 정보 및 권한\n"
        "- /status <area> — 영역 상태 요약\n"
        "- /env <area> — 환경 지표 조회\n"
        "- /open_door <area> — 문 열기 (사무실)\n\n"
        "그 외의 텍스트는 그대로 에코(echo) 됩니다."
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        await update.message.reply_text(update.message.text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("알 수 없는 명령어입니다. /help 를 확인해보세요.")


async def areas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cfg: BotConfig = context.bot_data.get("config")
    uid = get_user_id(update)
    available = [name for name, ac in cfg.areas.items() if uid in ac.members or uid in cfg.admins]
    if not available:
        await update.message.reply_text("접근 가능한 영역이 없습니다. 관리자를 통해 권한을 요청하세요.")
        return
    await update.message.reply_text("접근 가능 영역: " + ", ".join(sorted(available)))


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cfg: BotConfig = context.bot_data.get("config")
    user = update.effective_user
    if not user:
        await update.message.reply_text("사용자 정보를 확인할 수 없습니다.")
        return
    role = "admin" if user.id in cfg.admins else "member"
    await update.message.reply_text(
        f"ID: {user.id}\n이름: {user.full_name}\n역할: {role}"
    )


@guard(area_arg_index=0, command_name="status")
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    area = context.args[0].lower()
    # Compose environment from providers; simple priority order per area
    data = _get_env(area)
    text = (
        f"[{area}] 상태 요약\n"
        f"온도: {data.get('temperature')}°C, 습도: {data.get('humidity')}%\n"
        f"출처: {data.get('source')}"
    )
    await update.message.reply_text(text)


@guard(area_arg_index=0, command_name="env")
async def env(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    area = context.args[0].lower()
    data = _get_env(area)
    lines = [f"[{area}] 환경 지표"]
    for k, v in data.items():
        if k == "area":
            continue
        lines.append(f"- {k}: {v}")
    await update.message.reply_text("\n".join(lines))


@guard(area_arg_index=0, command_name="open_door")
async def open_door(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    area = context.args[0].lower()
    if area != "office":
        await update.message.reply_text("문 열기 기능은 'office' 에서만 지원됩니다.")
        return
    ok = tuya.open_door(area)
    await update.message.reply_text("문 열기 성공" if ok else "문 열기 실패")


def _get_env(area: str) -> dict:
    # Simple heuristic to choose provider by area
    src = "others"
    if area == "office":
        data = tuya.get_environment(area)
        src = "tuya"
    elif area == "server":
        data = smartthings.get_environment(area)
        src = "smartthings"
    elif area == "bedroom":
        data = lg_thinq.get_environment(area)
        src = "lg_thinq"
    else:
        data = others.get_environment(area)
    data.setdefault("source", src)
    return data


__all__ = [
    "start",
    "help_command",
    "echo",
    "unknown_command",
    "areas",
    "whoami",
    "status",
    "env",
    "open_door",
]
