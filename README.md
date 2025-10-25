% Python 텔레그램 봇 기본 틀 (Area 권한 관리 포함)

간단한 에코 기능과 `/start`, `/help` 명령을 포함한 최소 템플릿입니다.
`python-telegram-bot` (v21, asyncio) 기반으로 동작합니다.

## 요구사항
- Python 3.9 이상

## 설치 및 실행
1) 의존성 설치
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2) 토큰/설정
```bash
cp .env.example .env
# .env 파일을 열어 TELEGRAM_BOT_TOKEN 값을 실제 토큰으로 변경

# 권한/영역 설정 샘플 생성
cp config/bot.example.yaml config/bot.yaml
# config/bot.yaml 내 admins, areas.members 에 텔레그램 user id 등록
# 참고: /whoami 명령으로 내 user id 확인 가능
```

3) 실행
```bash
python main.py
# 또는
python -m main
```

## 명령어
- `/start` — 시작 안내 메시지
- `/help` — 사용 가능한 기능 설명
- `/areas` — 접근 가능한 영역 목록
- `/whoami` — 내 user id/역할 확인
- `/status <area>` — 영역 상태 요약
- `/env <area>` — 영역 환경 지표 (제공자별 결과)
- `/open_door <area>` — 문 열기 (office 전용, Tuya)
- 일반 텍스트 — 그대로 에코(echo)

## 파일 구조
```
.
├── main.py             # 엔트리포인트 (Application 초기화)
├── handlers.py         # 핸들러 함수 모음
├── auth.py             # 권한/가드 로직
├── bot_config.py       # YAML 로더 및 모델
├── providers/          # 통합 지점 (Tuya/LG/SmartThings/Others)
│   ├── tuya.py
│   ├── lg_thinq.py
│   ├── smartthings.py
│   └── others.py
├── config/
│   ├── bot.yaml         # 실제 설정 (로컬에서 생성)
│   └── bot.example.yaml # 샘플 설정
├── .env.example         # 환경변수 예시 (토큰)
├── requirements.txt     # 의존성 목록
└── README.md
```

## 커스터마이징 힌트
- 권한/영역: `config/bot.yaml`에서 admins, areas.members, areas.commands 관리
- 새 명령어 추가: `main.py`에 `CommandHandler("명령", 핸들러)` 추가 후 `auth.guard(...)`로 보호
- 통합 구현: `providers/`에 실제 SDK 연동 추가 (현재는 스텁)
- Webhook 전환: `Application.run_webhook(...)` 활용 (HTTPS 엔드포인트 필요)
