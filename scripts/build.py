"""Build the three pinned books, verify the assembled site and publish it to site/."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from check_site import PROJECTS, verify

ROOT = Path(__file__).resolve().parents[1]


def read_pins():
    pins = json.loads((ROOT / "sources.json").read_text())
    if len(pins) != len(PROJECTS) or {p["slug"] for p in pins} != PROJECTS:
        raise ValueError("sources.json must pin each project exactly once")
    for p in pins:
        if p["repository"] != f"urmzd/{p['slug']}" or not re.fullmatch(r"[0-9a-f]{40}", p["revision"]):
            raise ValueError(f"Invalid repository or commit for {p['slug']}")
    return pins


def build_book(pin, workspace, stage, local):
    slug = pin["slug"]
    source = str(local / slug) if local else f"https://github.com/{pin['repository']}.git"
    checkout = workspace / slug
    subprocess.run(["git", "init", "--quiet", str(checkout)], check=True)
    subprocess.run(["git", "fetch", "--quiet", "--no-tags", "--depth=1", source, pin["revision"]],
                   cwd=checkout, check=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", pin["revision"]], cwd=checkout, check=True)
    subprocess.run(["zensical", "build", "--clean", "--strict"], cwd=checkout, check=True)
    shutil.copytree(checkout / "site", stage / slug)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", type=Path, help="Read the pinned objects from local clones under this directory")
    args = parser.parse_args()
    local = args.local.resolve() if args.local else None
    pins = read_pins()
    with tempfile.TemporaryDirectory(prefix="docs-build-", dir=ROOT) as name:
        workspace = Path(name)
        stage = workspace / "assembled"
        shutil.copytree(ROOT / "public", stage)
        with ThreadPoolExecutor(max_workers=len(pins)) as workers:
            jobs = [workers.submit(build_book, p, workspace, stage, local) for p in pins]
            for job in jobs:
                job.result()
        verify(stage)
        output = ROOT / "site"
        if output.exists():
            output.rename(workspace / "previous-site")
        stage.rename(output)
    print(f"Ready at {output}")


if __name__ == "__main__":
    main()
