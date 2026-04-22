#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def sync_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def replace_file(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sync() -> None:
    if not DIST.exists():
        raise FileNotFoundError("dist directory does not exist, run build first")

    sync_dir(DIST / "blog", ROOT / "blog")
    sync_dir(DIST / "css", ROOT / "css")
    sync_dir(DIST / "js", ROOT / "js")

    replace_file(DIST / "index.html", ROOT / "index.html")
    replace_file(DIST / "archives.html", ROOT / "archives.html")
    replace_file(DIST / "about.html", ROOT / "about.html")
    replace_file(DIST / "CNAME", ROOT / "CNAME")

    print("Synced dist output into repository root")


if __name__ == "__main__":
    sync()
