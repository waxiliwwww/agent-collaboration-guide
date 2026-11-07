#!/usr/bin/env python3
"""Copy public skill files without reading, exporting, or replacing local/ data."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile

EXCLUDED = {"local", ".git", "__pycache__", ".installation.json"}


def public_files(source):
    source = Path(source).resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError("source must contain SKILL.md")
    files = []
    def scan_failed(error):
        raise error

    for directory, dirs, names in os.walk(source, followlinks=False, onerror=scan_failed):
        # Prune local/ before reading its contents, including a linked private root.
        dirs[:] = [d for d in dirs if d not in EXCLUDED]
        for name in dirs + names:
            path = Path(directory) / name
            if name in EXCLUDED or name.endswith(".pyc"):
                continue
            if path.is_symlink():
                raise ValueError(f"public symlink unsupported: {path.relative_to(source)}")
        for name in names:
            if name in EXCLUDED or name.endswith(".pyc"):
                continue
            path = Path(directory) / name
            files.append(path.relative_to(source))
    return source, sorted(files)


def update(source, target, init_local=False, dry_run=False):
    source, files = public_files(source)
    raw_target = Path(target).absolute()
    for component in [raw_target, *raw_target.parents]:
        if component.is_symlink():
            raise ValueError(f"target path must not contain a symlink: {component}")
    target = raw_target.resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("source and target must be separate directories")
    # Validate all destinations before changing any public file.
    for relative in files:
        for component in [target / relative, *(target / relative).parents]:
            if component.is_symlink():
                raise ValueError(f"destination symlink unsupported: {component}")
            if component == target:
                break
        destination = target / relative
        if destination.exists() and not destination.is_file():
            raise ValueError(f"public file destination is not a file: {relative}")
    preference = target / "local" / "preferences.md"
    if init_local and not preference.exists():
        private = target / "local"
        if private.is_symlink() or preference.is_symlink():
            raise ValueError("refusing to initialize through a private symlink")
        if private.exists() and not private.is_dir():
            raise ValueError("local must be a directory")
    if dry_run:
        return {"public_files": len(files), "local": "untouched", "dry_run": True}
    target.mkdir(parents=True, exist_ok=True)
    # Stage the complete input before replacing files. Never delete the target tree.
    with tempfile.TemporaryDirectory(prefix="skill-public-") as staging:
        staging = Path(staging)
        for relative in files:
            staged = staging / relative
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, staged)
        for relative in files:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as tmp:
                temporary = Path(tmp.name)
            try:
                shutil.copy2(staging / relative, temporary)
                os.replace(temporary, destination)
            finally:
                temporary.unlink(missing_ok=True)
    # Optional first-use creation; existing preferences, including linked roots, stay intact.
    if init_local and not (target / "local" / "preferences.md").exists():
        private = target / "local"
        private.mkdir(exist_ok=True)
        (private / "preferences.md").write_text(
            "# 本地用户偏好\n\n仅记录用户已确认的选择、范围和来源；"
            "本次任务细节留任务记录。暂无已记录的长期偏好。\n", encoding="utf-8"
        )
    return {"public_files": len(files), "local": "preserved"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="public source skill folder")
    parser.add_argument("target", type=Path, help="installation or export folder")
    parser.add_argument("--init-local", action="store_true", help="create missing private preference entry")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(update(args.source, args.target, args.init_local, args.dry_run), ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(1, f"skill update failed: {error}\n")


if __name__ == "__main__":
    main()
