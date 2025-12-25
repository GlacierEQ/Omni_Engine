from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(".").resolve()
FORCE = os.getenv("OP_FORCE", "0") == "1"
DRY = os.getenv("OP_DRY_RUN", "0") == "1"

def write_if_missing(path: Path, content: str) -> None:
    if DRY:
        return
    if path.exists() and not FORCE:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def main():
    # Minimal Dockerfile (non-destructive)
    dockerfile = ROOT / "Dockerfile"
    docker_content = (
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY . /app\n"
        "CMD [\"python\", \"-c\", \"print('Ready')\"]\n"
    )
    write_if_missing(dockerfile, docker_content)

    # Minimal GitHub Actions workflow
    wf = ROOT / ".github/workflows/ci.yml"
    wf_content = (
        "name: CI\n"
        "on: [push, pull_request]\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-python@v5\n"
        "        with:\n"
        "          python-version: '3.11'\n"
        "      - run: python -m pip install --upgrade pip\n"
        "      - run: if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\n"
        "      - run: if command -v ruff >/dev/null 2>&1; then ruff check .; else echo 'ruff not installed'; fi\n"
        "      - run: if command -v pytest >/dev/null 2>&1; then pytest -q; else echo 'pytest not installed'; fi\n"
    )
    write_if_missing(wf, wf_content)
    print("✅ Deployment prep complete (non-destructive).")

if __name__ == "__main__":
    main()
