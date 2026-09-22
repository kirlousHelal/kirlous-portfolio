"""Download demo images and videos into the Portfolio's local demos folder."""
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "demos"
USER = "kirlousHelal"
MEDIA_RE = re.compile(r"\.(png|jpe?g|gif|webp|bmp|svg|mp4|webm|mov|ogg)$", re.I)
VIDEO_RE = re.compile(r"\.(mp4|webm|mov|ogg)$", re.I)
README_RE = re.compile(
    r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|<img[^>]+src=[\"']([^\"']+)[\"']",
    re.I,
)

PROJECTS = {
    "cardiac": {
        "github": "Cardic-Function-Assement-GP---Flutter-DeepLearning_Computer_Vision-",
        "folders": ["Demo of The Mobile App", "Project_Images", "demo", "demos"],
    },
    "cloud": {
        "github": "Cloud-Computing-Project",
        "folders": ["Project_Images", "demo", "demos", "screenshots"],
    },
    "hotel": {
        "github": "Hotal-Rating---Machine-Learning",
        "folders": ["Project_Images", "demo", "demos", "screenshots"],
    },
    "cancer": {
        "github": "Multi_Cancer---Computer_Vision",
        "folders": ["Project_Images", "demo", "demos", "screenshots"],
    },
    "encryption": {
        "github": "Computer-Network-Security_-Full-package-MS1-MS2-MS3-",
        "folders": ["Project_Images", "demo", "demos", "screenshots"],
    },
    "social": {
        "github": "social_app_flutter",
        "folders": ["Project_Images", "demo", "demos"],
    },
    "shop": {
        "github": "shop_app_flutter",
        "folders": ["Project_Images", "demo", "demos"],
    },
    "bookly": {
        "github": "Bookly_Flutter_App",
        "folders": ["Project_Images", "demo", "demos"],
    },
    "news": {
        "github": "news_app_flutter",
        "folders": ["Project_Images", "demo", "demos"],
    },
    "buying": {
        "github": "BuyingApp-ITI_Mean-Stack",
        "folders": ["Project_Images", "demo", "demos", "screenshots"],
    },
}


def clone_repo(repo_name):
    repo_url = f"https://github.com/{USER}/{repo_name}.git"
    temp_dir = Path(tempfile.mkdtemp(prefix="portfolio-demo-"))
    result = subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(temp_dir / "repo")],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git clone failed")
    return temp_dir / "repo"


def collect_repo_media(repo_dir):
    found = {}
    for path in repo_dir.rglob("*"):
        if path.is_file() and MEDIA_RE.search(path.name):
            rel = path.relative_to(repo_dir).as_posix()
            found[rel] = path

    for readme in repo_dir.rglob("README*"):
        if not readme.is_file():
            continue
        try:
            text = readme.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for match in README_RE.finditer(text):
            for group in match.groups():
                if not group:
                    continue
                item = group.strip()
                if item.startswith("http://") or item.startswith("https://"):
                    if MEDIA_RE.search(item):
                        found[f"readme:{item}"] = item
                    continue
                candidate = (readme.parent / item).resolve()
                if candidate.exists() and candidate.is_file() and MEDIA_RE.search(candidate.name):
                    rel = candidate.relative_to(repo_dir.resolve()).as_posix()
                    found[rel] = candidate
    return found


def safe_name(name, used):
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name).strip() or "file"
    stem, ext = Path(cleaned).stem, Path(cleaned).suffix
    candidate = cleaned
    n = 2
    while candidate.lower() in used:
        candidate = f"{stem}-{n}{ext}"
        n += 1
    used.add(candidate.lower())
    return candidate


def download_url(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "portfolio-demo-downloader"})
    with urllib.request.urlopen(req, timeout=180) as res:
        data = res.read()
    if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
        raise RuntimeError("Git LFS pointer")
    dest.write_bytes(data)
    return len(data)


def main():
    OUT.mkdir(exist_ok=True)
    manifest = {}

    for pid, meta in PROJECTS.items():
        repo_name = meta["github"]
        print(f"\n=== {pid} / {repo_name}")

        repo_dir = None
        try:
            repo_dir = clone_repo(repo_name)
            found = collect_repo_media(repo_dir)
        except Exception as exc:
            print(f"  clone failed: {exc}")
            found = {}

        dest_dir = OUT / pid
        dest_dir.mkdir(exist_ok=True, parents=True)
        used = set()
        items = []

        for key, source in found.items():
            try:
                if isinstance(source, Path):
                    filename = safe_name(source.name, used)
                    dest = dest_dir / filename
                    shutil.copy2(source, dest)
                    size = dest.stat().st_size
                    kind = "video" if VIDEO_RE.search(filename) else "image"
                    items.append({
                        "name": Path(filename).stem,
                        "file": f"demos/{pid}/{filename}",
                        "kind": kind,
                    })
                    print(f"  copied {filename} ({size} bytes)")
                else:
                    filename = safe_name(Path(key.split("/", 1)[-1].split("?", 1)[0]).name or "image", used)
                    dest = dest_dir / filename
                    size = download_url(source, dest)
                    kind = "video" if VIDEO_RE.search(filename) else "image"
                    items.append({
                        "name": Path(filename).stem,
                        "file": f"demos/{pid}/{filename}",
                        "kind": kind,
                    })
                    print(f"  downloaded {filename} ({size} bytes)")
            except Exception as exc:
                print(f"  skip {key}: {exc}")

        manifest[pid] = items
        print(f"  total {len(items)}")

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nWrote demos/manifest.json")


if __name__ == "__main__":
    main()
