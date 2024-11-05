from pathlib import Path

from custom_tasker.main import keybind_task_sequence

ROOT_DIR = Path(__file__).parent

if __name__ == "__main__":
    keybind_task_sequence(ROOT_DIR / "task_config" / "auction_house.json")
