#!/usr/bin/env python3
"""
sync_to_wechat.py — Hugo Blog → 微信公众号草稿同步工具

用法：
  # 指定文章目录（包含 index.md）
  python3 sync_to_wechat.py --post-dir /path/to/blog/content/blog/2026/0311-xxx

  # 指定单个 markdown 文件
  python3 sync_to_wechat.py --post-file /path/to/index.md

环境变量：
  WX_APPID      微信公众号 AppID
  WX_APPSECRET  微信公众号 AppSecret

依赖：pip install requests markdown
"""

import os
import sys
import re
import json
import time
import argparse
import textwrap
from pathlib import Path

import requests

# ── 微信 API ──────────────────────────────────────────
WX_API = "https://api.weixin.qq.com/cgi-bin"
APPID     = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")

# ── Token 缓存（同一进程复用） ─────────────────────────
_access_token = None
_token_expires = 0


def get_access_token() -> str:
    global _access_token, _token_expires
    if _access_token and time.time() < _token_expires - 60:
        return _access_token
    url = f"{WX_API}/token"
    r = requests.get(url, params={
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET,
    }, timeout=10)
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"获取 access_token 失败: {data}")
    _access_token = data["access_token"]
    _token_expires = time.time() + data.get("expires_in", 7200)
    print(f"[WX] access_token 获取成功，有效期 {data.get('expires_in', 7200)}s")
    return _access_token


# ── 解析 Hugo Front Matter ─────────────────────────────
def parse_front_matter(text: str) -> tuple[dict, str]:
    """返回 (meta dict, body markdown)"""
    meta = {}
    body = text
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if m:
        fm_raw, body = m.group(1), m.group(2)
        for line in fm_raw.splitlines():
            kv = line.split(":", 1)
            if len(kv) == 2:
                k = kv[0].strip()
                v = kv[1].strip().strip('"').strip("'")
                meta[k] = v
    return meta, body


# ── Markdown → 微信友好 HTML ──────────────────────────
def md_to_wx_html(md_text: str, base_url: str = "https://helight.cn") -> str:
    """
    把 Markdown 转成微信公众号可用的 HTML。
    微信不支持 CSS class / JS，只接受内联样式。
    """
    try:
        import markdown as md_lib
        html = md_lib.markdown(
            md_text,
            extensions=["tables", "fenced_code", "toc", "nl2br"],
        )
    except ImportError:
        # fallback: 简单替换
        html = simple_md_to_html(md_text)

    # 补充内联样式，让微信排版好看
    style_map = [
        (r'<h1([^>]*)>', r'<h1\1 style="font-size:24px;font-weight:bold;margin:20px 0 10px;color:#1a1a1a;">'),
        (r'<h2([^>]*)>', r'<h2\1 style="font-size:20px;font-weight:bold;margin:18px 0 8px;color:#1a1a1a;border-left:4px solid #07C160;padding-left:10px;">'),
        (r'<h3([^>]*)>', r'<h3\1 style="font-size:17px;font-weight:bold;margin:14px 0 6px;color:#333;">'),
        (r'<p([^>]*)>',  r'<p\1 style="line-height:1.8;margin:8px 0;color:#333;font-size:16px;">'),
        (r'<ul([^>]*)>', r'<ul\1 style="padding-left:20px;margin:8px 0;">'),
        (r'<ol([^>]*)>', r'<ol\1 style="padding-left:20px;margin:8px 0;">'),
        (r'<li([^>]*)>', r'<li\1 style="line-height:1.8;margin:4px 0;color:#333;font-size:16px;">'),
        (r'<code([^>]*)>',r'<code\1 style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-family:monospace;font-size:14px;color:#d63384;">'),
        (r'<pre([^>]*)>', r'<pre\1 style="background:#f8f8f8;padding:16px;border-radius:6px;overflow-x:auto;font-size:14px;line-height:1.6;margin:12px 0;">'),
        (r'<blockquote([^>]*)>', r'<blockquote\1 style="border-left:4px solid #07C160;padding:8px 16px;margin:12px 0;background:#f9f9f9;color:#555;">'),
        (r'<table([^>]*)>', r'<table\1 style="border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;">'),
        (r'<th([^>]*)>',  r'<th\1 style="border:1px solid #ddd;padding:8px;background:#f2f2f2;font-weight:bold;text-align:left;">'),
        (r'<td([^>]*)>',  r'<td\1 style="border:1px solid #ddd;padding:8px;">'),
        (r'<a ([^>]*)href="([^"]*)"([^>]*)>',
         r'<a \1href="\2"\3 style="color:#07C160;text-decoration:none;">'),
        (r'<strong([^>]*)>', r'<strong\1 style="font-weight:bold;color:#1a1a1a;">'),
        (r'<em([^>]*)>',    r'<em\1 style="font-style:italic;color:#555;">'),
        (r'<hr([^>]*)>',    r'<hr\1 style="border:none;border-top:1px solid #eee;margin:20px 0;">'),
    ]
    for pattern, repl in style_map:
        html = re.sub(pattern, repl, html)

    # 底部署名
    footer = (
        '<p style="margin-top:40px;padding-top:16px;border-top:1px solid #eee;'
        'color:#999;font-size:13px;text-align:center;">'
        f'原文发布于 <a href="{base_url}" style="color:#07C160;">{base_url}</a> '
        '· 转载请注明出处</p>'
    )
    html = html + footer
    return html


def simple_md_to_html(md_text: str) -> str:
    """无 markdown 库时的简易转换"""
    lines = md_text.splitlines()
    out = []
    for line in lines:
        if line.startswith("### "):
            out.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- ") or line.startswith("* "):
            out.append(f"<li>{line[2:]}</li>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{line[2:]}</blockquote>")
        elif line.strip() == "---":
            out.append("<hr>")
        elif line.strip():
            out.append(f"<p>{line}</p>")
    return "\n".join(out)


# ── 上传封面图 ─────────────────────────────────────────
def upload_thumb(image_path: str) -> str | None:
    """上传缩略图素材，返回 media_id"""
    if not image_path or not Path(image_path).exists():
        return None
    token = get_access_token()
    url = f"{WX_API}/media/upload?access_token={token}&type=thumb"
    with open(image_path, "rb") as f:
        files = {"media": (Path(image_path).name, f, "image/jpeg")}
        r = requests.post(url, files=files, timeout=20)
    data = r.json()
    if "media_id" in data:
        print(f"[WX] 封面图上传成功: media_id={data['media_id']}")
        return data["media_id"]
    print(f"[WX] 封面图上传失败: {data}")
    return None


# ── 创建草稿 ───────────────────────────────────────────
def create_draft(title: str, content_html: str,
                 author: str = "helight",
                 digest: str = "",
                 thumb_media_id: str = "") -> dict:
    """创建公众号草稿，返回 API 响应"""
    token = get_access_token()
    url = f"{WX_API}/draft/add?access_token={token}"

    article = {
        "title": title,
        "author": author,
        "digest": digest[:120] if digest else "",   # 摘要最多120字
        "content": content_html,
        "content_source_url": "https://helight.cn",
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id

    payload = {"articles": [article]}
    r = requests.post(url, json=payload, timeout=15)
    return r.json()


# ── 主流程 ─────────────────────────────────────────────
def sync_post(post_path: Path) -> dict:
    """
    同步一篇文章到微信公众号草稿。
    post_path: index.md 文件路径
    返回: {"media_id": ..., "url": ...}
    """
    if not APPID or not APPSECRET:
        raise RuntimeError("请设置环境变量 WX_APPID 和 WX_APPSECRET")

    text = post_path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)

    title   = meta.get("title", post_path.parent.name)
    author  = meta.get("author", "helight")
    digest  = meta.get("summary", "")
    banner  = meta.get("banner", "")

    print(f"[SYNC] 文章标题: {title}")
    print(f"[SYNC] 摘要: {digest[:60]}...")

    # 封面图：优先找本地 banner
    thumb_id = None
    if banner:
        # banner 格式: /blog/2026/0311-xxx/imgs/xxx.jpg
        # 本地路径在 hxblog 仓库内
        local_banner = None
        post_dir = post_path.parent
        # 查找 post_dir 下的图片
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            imgs = list(post_dir.rglob(ext))
            if imgs:
                local_banner = str(imgs[0])
                break
        if local_banner:
            thumb_id = upload_thumb(local_banner)

    # Markdown → HTML
    html = md_to_wx_html(body)

    # 创建草稿
    result = create_draft(
        title=title,
        content_html=html,
        author=author,
        digest=digest,
        thumb_media_id=thumb_id or "",
    )

    if "media_id" in result:
        draft_url = f"https://mp.weixin.qq.com/cgi-bin/appmsgmasssend?action=draft&lang=zh_CN"
        print(f"[WX] ✅ 草稿创建成功！media_id={result['media_id']}")
        print(f"[WX] 👉 登录公众号后台审阅并发布: {draft_url}")
        return result
    else:
        raise RuntimeError(f"草稿创建失败: {result}")


def find_latest_post(blog_root: Path) -> Path | None:
    """找最近一次修改的 index.md"""
    posts = sorted(
        blog_root.rglob("index.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return posts[0] if posts else None


def main():
    parser = argparse.ArgumentParser(description="Hugo Blog → 微信公众号草稿同步")
    parser.add_argument("--post-dir",  help="文章目录（含 index.md）")
    parser.add_argument("--post-file", help="直接指定 index.md 路径")
    parser.add_argument("--blog-root", default="/projects/hxblog/content/blog",
                        help="Hugo blog 内容根目录（用于自动寻找最新文章）")
    parser.add_argument("--latest",    action="store_true",
                        help="自动同步最新一篇文章")
    args = parser.parse_args()

    if args.post_file:
        post_path = Path(args.post_file)
    elif args.post_dir:
        post_path = Path(args.post_dir) / "index.md"
    elif args.latest:
        post_path = find_latest_post(Path(args.blog_root))
        if not post_path:
            print("未找到任何文章", file=sys.stderr)
            sys.exit(1)
        print(f"[SYNC] 自动选择最新文章: {post_path}")
    else:
        parser.print_help()
        sys.exit(1)

    if not post_path.exists():
        print(f"文件不存在: {post_path}", file=sys.stderr)
        sys.exit(1)

    result = sync_post(post_path)
    # 输出 JSON 供 CI 读取
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
