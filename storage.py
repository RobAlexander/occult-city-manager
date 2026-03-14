"""
Save and load cities to/from JSON files.
"""
import json
import os
from pathlib import Path
from models import City

SAVE_DIR = Path("cities")


def save_city(city: City, directory: Path = SAVE_DIR) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    filename = directory / f"{city.name.lower().replace(' ', '_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(city.to_dict(), f, indent=2, ensure_ascii=False)
    return filename


def load_city(filename: str | Path) -> City:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return City.from_dict(data)


def list_cities(directory: Path = SAVE_DIR) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))
