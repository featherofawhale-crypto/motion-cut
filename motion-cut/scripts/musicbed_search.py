#!/usr/bin/env python3
"""Musicbed / 环球(UPM) 检索通路（0827 实测，均无需登录、无需浏览器）。

  python3 musicbed_search.py mb "cinematic corporate" [--preview N --out DIR]
  python3 musicbed_search.py upm "cinematic" [--locale en-hk]

Musicbed: POST novus-api.musicbed.com/api/search/songs，返回 JSON 全字段
（曲名/艺人/时长/流派/BPM keys/30s 试听直链）。30s 试听 mp3 可直接下载；
全长 preview 端点 401 需登录，属正常边界。
UPM: GET universalproductionmusic.com/<locale>/search?query=... SSR 页面，
解析 itemprop 元数据（id/曲名/关键词/时长）。试听音频 CDN 403，需浏览器。
"""
import argparse, json, re, subprocess, sys, pathlib

UA = "Mozilla/5.0"

def curl(args, url, extra=None):
    # UPM SSR 页面偶发 40s+ 慢响应，放宽到 120s
    cmd = ["curl", "-sL", "-A", UA, "--max-time", "120"] + (extra or []) + [url]
    return subprocess.run(cmd, capture_output=True, check=True).stdout

def mb(query, preview_n, out):
    body = json.dumps({"query": query, "limit": 20})
    raw = curl([], "https://novus-api.musicbed.com/api/search/songs?order=default",
               ["-X", "POST", "-H", "Content-Type: application/json", "-d", body])
    data = json.loads(raw)
    songs = data.get("data", [])
    if not songs:
        print("无结果", file=sys.stderr); sys.exit(1)
    for i, s in enumerate(songs, 1):
        genres = ",".join(g.get("name", "") for g in s.get("genres", []))
        artist = (s.get("album") or {}).get("artist", {}).get("name", "?")
        print(f"{i:02d}. {s['name']} | {artist} | {s.get('length','?')} | {genres} | "
              f"https://www.musicbed.com/songs/{s['slug']}/{s['id']}")
        if i <= preview_n and s.get("playback_url"):
            out.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^A-Za-z0-9]+", "", s["name"].title())[:40]
            dst = out / f"MUS_Musicbed_{i:02d}_{safe}_30sPrev_LOGIN_GATED.mp3"
            dst.write_bytes(curl([], s["playback_url"]))
            print(f"    -> {dst} ({dst.stat().st_size} bytes, 30s 试听, 全长需登录)")

def upm(query, locale):
    raw = curl([], f"https://www.universalproductionmusic.com/{locale}/search?query="
                  + re.sub(r"\s+", "%20", query)).decode("utf-8", "replace")
    ids = re.findall(r'itemprop="identifier" content="(\d+)"', raw)
    names = re.findall(r'itemprop="name" content="([^"]+)"', raw)
    durs = re.findall(r'itemprop="duration" content="([0-9:]+)"', raw)
    if not ids:
        print("无结果", file=sys.stderr); sys.exit(1)
    for i, (tid, name, dur) in enumerate(list(zip(ids, names, durs))[:20], 1):
        print(f"{i:02d}. {name} | {dur} | id={tid} | "
              f"https://www.universalproductionmusic.com/{locale}/track/{tid}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site", choices=["mb", "upm"])
    ap.add_argument("query")
    ap.add_argument("--preview", type=int, default=0)
    ap.add_argument("--out", default=".")
    ap.add_argument("--locale", default="en-hk")
    a = ap.parse_args()
    if a.site == "mb":
        mb(a.query, a.preview, pathlib.Path(a.out))
    else:
        upm(a.query, a.locale)

if __name__ == "__main__":
    main()
