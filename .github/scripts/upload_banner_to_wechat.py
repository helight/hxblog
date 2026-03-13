#!/usr/bin/env python3
"""
upload_banner_to_wechat.py — 自动上传 blog banner 图到微信公众号素材库

PR 合并后自动触发，将文章 banner 图上传为微信永久图片素材，
方便在公众号后台直接选用。

用法：
  python3 upload_banner_to_wechat.py --post-dir /path/to/blog/content/blog/2026/0311-xxx
  python3 upload_banner_to_wechat.py --post-file /path/to/index.md
  python3 upload_banner_to_wechat.py --image /path/to/banner.jpg --title "文章标题"

环境变量：
  WX_APPID      微信公众号 AppID
  WX_APPSECRET  微信公众号 AppSecret
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path

import requests

WX_API    = "https://api.weixin.qq.com/cgi-bin"
APPID     = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")

_access_token   = None
_token_expires  = 0


def get_access_token() -> str:
    global _access_token, _token_expires
    if _access_token and time.time() < _token_expires - 60:
        return _access_token
    r = requests.get(f"{WX_API}/token", params={
        "grant_type": "client_credential",
        "appid": APPID, "secret": APPSECRET,
    }, timeout=10)
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"获取 access_token 失败: {data}")
    _access_token  = data["access_token"]
    _token_expires = time.time() + data.get("expires_in", 7200)
    print(f"[WX] access_token 获取成功")
    return _access_token


def upload_image_material(image_path: str, title: str = "") -> dict:
    """
    上传图片为微信永久图片素材（type=image）。
    返回 {"media_id": "...", "url": "..."}
    注意：type=image 可获得可访问的 URL，可直接在文章里引用。
    """
    token = get_access_token()
    url   = f"{WX_API}/material/add_material?access_token={token}&type=image"

    img   = Path(image_path)
    mime  = "image/jpeg" if img.suffix.lower() in (".jpg", ".jpeg") else "image/png"

    with open(image_path, "rb") as f:
        # description 字段：title + introduction
        desc = json.dumps({"title": title or img.stem, "introduction": title or img.stem},
                          ensure_ascii=False)
        files   = {"media": (img.name, f, mime)}
        data    = {"description": desc}
        r = requests.post(url, files=files, data=data, timeout=30)

    result = r.json()
    if "media_id" in result:
        media_id = result["media_id"]
        wx_url   = result.get("url", "")
        print(f"[WX] ✅ 图片上传成功!")
        print(f"[WX]    media_id : {media_id}")
        print(f"[WX]    图片URL  : {wx_url}")
        return {"media_id": media_id, "url": wx_url}
    else:
        raise RuntimeError(f"图片上传失败: {result}")


def parse_front_matter(text: str) -> tuple[dict, str]:
    meta = {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            kv = line.split(":", 1)
            if len(kv) == 2:
                meta[kv[0].strip()] = kv[1].strip().strip('"').strip("'")
    return meta


def find_banner(post_dir: Path) -> Path | None:
    """在文章目录下找 banner 图"""
    for pattern in ("imgs/banner.*", "imgs/*.jpg", "imgs/*.jpeg", "imgs/*.png", "*.jpg", "*.png"):
        imgs = sorted(post_dir.glob(pattern))
        if imgs:
            return imgs[0]
    return None


def sync_banner(post_path: Path) -> dict:
    if not APPID or not APPSECRET:
        raise RuntimeError("请设置环境变量 WX_APPID 和 WX_APPSECRET")

    text   = post_path.read_text(encoding="utf-8")
    meta   = parse_front_matter(text)
    title  = meta.get("title", post_path.parent.name)

    print(f"[SYNC] 文章: {title}")

    banner = find_banner(post_path.parent)
    if not banner:
        raise FileNotFoundError(f"未找到 banner 图: {post_path.parent}/imgs/")

    print(f"[SYNC] Banner: {banner}  ({banner.stat().st_size // 1024} KB)")
    return upload_image_material(str(banner), title)


def main():
    parser = argparse.ArgumentParser(description="上传 blog banner 到微信公众号素材库")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--post-dir",  help="文章目录（含 index.md）")
    g.add_argument("--post-file", help="直接指定 index.md 路径")
    g.add_argument("--image",     help="直接指定图片路径")
    parser.add_argument("--title", default="", help="素材标题（配合 --image 使用）")
    args = parser.parse_args()

    if args.image:
        result = upload_image_material(args.image, args.title)
    else:
        if args.post_file:
            post_path = Path(args.post_file)
        else:
            post_path = Path(args.post_dir) / "index.md"

        if not post_path.exists():
            print(f"文件不存在: {post_path}", file=sys.stderr)
            sys.exit(1)
        result = sync_banner(post_path)

    print(f"\n[DONE] 上传完成，前往公众号后台素材库选用：")
    print(f"       https://mp.weixin.qq.com/cgi-bin/appmsgpicture")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
