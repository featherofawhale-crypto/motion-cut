#!/usr/bin/env python3
"""Mixkit 免费音乐检索 + 下载（0827 实测通路，无需浏览器/登录）。

用法:
  python3 mixkit_search.py <tag或关键词> [--download N --out DIR]

Mixkit 列表页内嵌 JSON-LD ItemList，含曲名/流派/作者/时长/mp3 直链/授权声明。
tag 示例: corporate, cinematic, ambient, technology（对应 /free-stock-music/tag/<tag>/）
授权: Mixkit Stock Music Free License，商用免费、无需署名（以 license 页为准）。
"""
import argparse, json, re, subprocess, sys, pathlib

UA = {"User-Agent": "Mozilla/5.0"}

def fetch(url: str) -> str:
    # 用 curl 而不是 urllib：macOS 框架版 Python 常缺 CA 证书，curl 走系统钥匙串
    return subprocess.run(
        ["curl", "-sL", "-A", UA["User-Agent"], url],
        capture_output=True, check=True, timeout=60,
    ).stdout.decode("utf-8", "replace")

def download(url: str, dst: pathlib.Path):
    subprocess.run(
        ["curl", "-sL", "-A", UA["User-Agent"], "-o", str(dst), url],
        check=True, timeout=120,
    )

def parse_tracks(html: str):
    tracks = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                if o.get("@type") == "ItemList":
                    for e in o.get("itemListElement", []):
                        if e.get("@type") == "MusicRecording" and e.get("url", "").endswith(".mp3"):
                            tracks.append({
                                "name": e.get("name"), "genre": e.get("genre"),
                                "artist": e.get("byArtist"), "duration": e.get("duration"),
                                "mp3": e.get("url"),
                                "license": e.get("copyrightNotice", "Mixkit Stock Music Free License"),
                            })
                stack.extend(o.values())
            elif isinstance(o, list):
                stack.extend(o)
    return tracks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", help="Mixkit tag，如 corporate / cinematic / ambient")
    ap.add_argument("--download", type=int, default=0, help="下载前 N 首")
    ap.add_argument("--out", default=".", help="下载目录")
    args = ap.parse_args()

    url = f"https://mixkit.co/free-stock-music/tag/{args.tag}/"
    html = fetch(url)
    tracks = parse_tracks(html)
    if not tracks:
        print(f"未解析到曲目，tag 可能不存在: {url}", file=sys.stderr)
        sys.exit(1)

    out = pathlib.Path(args.out)
    for i, t in enumerate(tracks, 1):
        print(f"{i:02d}. {t['name']} | {t['genre']} | {t['artist']} | {t['duration']} | {t['mp3']}")
        if i <= args.download:
            out.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^A-Za-z0-9]+", "", t["name"].title())
            dst = out / f"MUS_Mixkit_{i:02d}_{safe}_Free.mp3"
            download(t["mp3"], dst)
            print(f"    -> {dst} ({dst.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
