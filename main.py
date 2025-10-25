from __future__ import annotations

import logging
import os
import sys

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers import (
    echo,
    help_command,
    start,
    unknown_command,
    areas,
    whoami,
    status,
    env,
    open_door,
)
from bot_config import load_config


def main() -> None:
    # Load .env if present
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("[ERROR] TELEGRAM_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
        print(".env 파일을 생성하거나 환경 변수로 토큰을 설정하세요.")
        sys.exit(1)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Load access control config
    cfg = load_config()

    app = Application.builder().token(token).build()
    # Share config via bot_data for auth checks
    app.bot_data["config"] = cfg

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("areas", areas))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("env", env))
    app.add_handler(CommandHandler("open_door", open_door))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Start polling
    logging.info("Starting bot polling...")
    app.run_polling(allowed_updates=None, close_loop=False)


if __name__ == "__main__":
    main()
