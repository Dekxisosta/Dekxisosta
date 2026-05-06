import os
import base64
import urllib.request
import urllib.parse
import json
from datetime import datetime, timezone

CLIENT_ID     = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["SPOTIFY_REFRESH_TOKEN"]

OUTPUT_PATH = "spotify.svg"
TRACK_COUNT = 3

def get_access_token():
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    data = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN}).encode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={"Authorization": f"Basic {credentials}", "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read())["access_token"]
    except urllib.error.HTTPError as e:
        print("Spotify error:", e.read().decode())
        raise

def get_recently_played(token):
    req = urllib.request.Request(
        f"https://api.spotify.com/v1/me/player/recently-played?limit={TRACK_COUNT}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as res:
        items = json.loads(res.read())["items"]

    tracks = []
    for item in items:
        track   = item["track"]
        played  = item["played_at"]  # ISO 8601
        name    = track["name"]
        artist  = ", ".join(a["name"] for a in track["artists"])
        img_url = track["album"]["images"][-1]["url"]  # smallest image
        tracks.append({"name": name, "artist": artist, "img_url": img_url, "played_at": played})
    return tracks

def fetch_image_b64(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        raw = res.read()
    return base64.b64encode(raw).decode()

def time_ago(iso: str) -> str:
    played = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    diff   = int((datetime.now(timezone.utc) - played).total_seconds())
    if diff < 60:
        return "just now"
    if diff < 3600:
        m = diff // 60
        return f"{m} minute{'s' if m != 1 else ''} ago"
    if diff < 86400:
        h = diff // 3600
        return f"{h} hour{'s' if h != 1 else ''} ago"
    d = diff // 86400
    return f"{d} day{'s' if d != 1 else ''} ago"

ROW_H    = 72  
PADDING  = 24
IMG_SIZE = 48
TOP      = 52 

def truncate(text: str, limit: int = 30) -> str:
    return text if len(text) <= limit else text[:limit - 1] + "…"

def build_svg(tracks: list) -> str:
    height = TOP + len(tracks) * ROW_H + PADDING

    rows = ""
    for i, t in enumerate(tracks):
        y      = TOP + i * ROW_H
        img_b64 = fetch_image_b64(t["img_url"])
        dot_fill = "#f0a8d0" if i == 0 else "#9b7cb8"

        rows += f"""
  <line x1="{PADDING}" y1="{y}" x2="{680 - PADDING}" y2="{y}" stroke="#2d1f45" stroke-width="0.5"/>
  <g transform="translate({PADDING},{y + 12})">
    <image href="data:image/jpeg;base64,{img_b64}" x="0" y="0" width="{IMG_SIZE}" height="{IMG_SIZE}" clip-path="url(#clip{i})"/>
    <text x="64" y="16"  font-family="sans-serif" font-size="13" font-weight="600" fill="#f5e6ff">{truncate(t['name'])}</text>
    <text x="64" y="32"  font-family="sans-serif" font-size="11" fill="#c9a8e0">{truncate(t['artist'], 35)}</text>
    <text x="64" y="46"  font-family="sans-serif" font-size="10" fill="#9b7cb8">{time_ago(t['played_at'])}</text>
    <circle cx="{680 - PADDING * 2}" cy="24" r="3" fill="{dot_fill}"/>
  </g>"""

    clip_defs = "".join(
        f'<clipPath id="clip{i}"><rect x="0" y="0" width="{IMG_SIZE}" height="{IMG_SIZE}" rx="6"/></clipPath>'
        for i in range(len(tracks))
    )

    return f"""<svg width="680" height="{height}" viewBox="0 0 680 {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>{clip_defs}</defs>
  <rect width="680" height="{height}" rx="16" fill="#120b22"/>
  <text x="{PADDING}" y="30" font-family="sans-serif" font-size="12" font-weight="600" fill="#f0a8d0" letter-spacing="0.08em">&#127925;  recently played</text>
{rows}
</svg>"""

if __name__ == "__main__":
    print("Fetching access token...")
    token  = get_access_token()

    print("Fetching recently played tracks...")
    tracks = get_recently_played(token)

    for t in tracks:
        print(f"  ✓ {t['name']} — {t['artist']} ({time_ago(t['played_at'])})")

    print("Generating SVG...")
    svg = build_svg(tracks)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Saved to {OUTPUT_PATH}")
