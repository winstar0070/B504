from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

import yaml


@dataclass
class AreaConfig:
    members: Set[int] = field(default_factory=set)
    commands: Set[str] = field(default_factory=set)


@dataclass
class BotConfig:
    admins: Set[int] = field(default_factory=set)
    areas: Dict[str, AreaConfig] = field(default_factory=dict)
    default_commands: Set[str] = field(default_factory=lambda: {"status", "env"})

    def users_for_area(self, area: str) -> Set[int]:
        cfg = self.areas.get(area)
        return cfg.members if cfg else set()

    def commands_for_area(self, area: str) -> Set[str]:
        cfg = self.areas.get(area)
        if cfg and cfg.commands:
            return cfg.commands
        return self.default_commands


def _as_int_set(items: Optional[List[int]]) -> Set[int]:
    return {int(x) for x in items or []}


def _as_str_set(items: Optional[List[str]]) -> Set[str]:
    return {str(x) for x in items or []}


def load_config(path: Optional[str] = None) -> BotConfig:
    """Load YAML config from path or default location.

    Search order:
    - explicit path
    - env BOT_CONFIG (file path)
    - ./config/bot.yaml
    - ./config/bot.example.yaml (fallback for local dev)
    """
    candidates = []
    if path:
        candidates.append(path)
    env_path = os.getenv("BOT_CONFIG")
    if env_path:
        candidates.append(env_path)
    candidates.append(os.path.join("config", "bot.yaml"))
    candidates.append(os.path.join("config", "bot.example.yaml"))

    cfg_path = next((p for p in candidates if os.path.exists(p)), None)
    if not cfg_path:
        # empty defaults when no config found
        return BotConfig()

    with open(cfg_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    admins = _as_int_set(raw.get("admins"))

    areas: Dict[str, AreaConfig] = {}
    raw_areas = raw.get("areas", {}) or {}
    for name, acfg in raw_areas.items():
        members = _as_int_set(acfg.get("members"))
        commands = _as_str_set(acfg.get("commands"))
        areas[name] = AreaConfig(members=members, commands=commands)

    default_commands = _as_str_set((raw.get("defaults") or {}).get("commands")) or {"status", "env"}

    return BotConfig(admins=admins, areas=areas, default_commands=default_commands)

