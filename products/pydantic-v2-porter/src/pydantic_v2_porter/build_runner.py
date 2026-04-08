from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


def build_project(root: Path) -> list[str]:
    temp_root = root / "pydantic_v2_porter_tmp"
    temp_root.mkdir(exist_ok=True)

    os.environ["TMP"] = str(temp_root)
    os.environ["TEMP"] = str(temp_root)
    os.environ["TMPDIR"] = str(temp_root)
    tempfile.tempdir = str(temp_root)

    artifacts: list[str] = []
    for top_level in ("src", "tests"):
        base = root / top_level
        if not base.exists():
            continue

        for source_file in sorted(base.rglob("*.py")):
            source = source_file.read_text(encoding="utf-8-sig")
            compile(source, str(source_file), "exec")
            artifacts.append(str(source_file.relative_to(root)))

    return artifacts


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[0]).resolve() if argv else Path.cwd().resolve()
    artifacts = build_project(root)
    for artifact in artifacts:
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
