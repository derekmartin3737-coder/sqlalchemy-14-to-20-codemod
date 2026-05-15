from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    for path in sorted(root.rglob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
