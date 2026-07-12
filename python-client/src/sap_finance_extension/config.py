from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "local-data"
