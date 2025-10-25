from __future__ import annotations

import os
from typing import Dict, Any


def open_door(area: str) -> bool:
    """Open door for a given area using Tuya integration.
    TODO: Implement real call. This is a stub.
    """
    # Example: use env creds (replace with real SDK usage)
    _ = os.getenv("TUYA_ACCESS_ID"), os.getenv("TUYA_ACCESS_SECRET"), os.getenv("TUYA_ENDPOINT")
    # Return success for demo
    return area.lower() == "office"


def get_environment(area: str) -> Dict[str, Any]:
    """Return environment metrics for area (stub)."""
    return {
        "area": area,
        "temperature": 23.1,
        "humidity": 41.8,
        "co2": 620,
        "source": "tuya",
    }

