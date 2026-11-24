"""读取 config/config.toml。"""

import os
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.toml"


def load_config() -> dict:
    with CONFIG_PATH.open("rb") as handle:
        return tomllib.load(handle)


def resolve_api_key(config: dict | None = None) -> str:
    config = config or load_config()
    key = str(config.get("model", {}).get("api_key") or "").strip()
    if key:
        return key
    return os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""


def csv_path(config: dict | None = None) -> Path:
    config = config or load_config()
    return PROJECT_ROOT / config["data"]["csv"]
