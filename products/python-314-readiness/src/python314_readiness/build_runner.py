from __future__ import annotations

from pathlib import Path


def main() -> int:
    src = Path(__file__).resolve().parents[1]
    for path in src.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
