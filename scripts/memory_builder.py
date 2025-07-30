import json
from pathlib import Path

CONFIG_FILE = Path('memory_constellation.json')


def load_config(path: Path) -> dict:
    """Load JSON configuration."""
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def create_directories(paths):
    """Create directories if they do not exist."""
    for p in paths:
        directory = Path(p)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")


def main():
    if not CONFIG_FILE.exists():
        print(f"Config file {CONFIG_FILE} not found.")
        return

    config = load_config(CONFIG_FILE)
    directories = config.get('directories', [])
    if not directories:
        print("No directories specified in config.")
        return

    create_directories(directories)


if __name__ == '__main__':
    main()
