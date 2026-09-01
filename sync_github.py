#!/usr/bin/env python3
"""
StarShack 官网 → GitHub 增量同步脚本

为什么需要它：
  本机 git 走本地代理（http_proxy=127.0.0.1:547xx）时，HTTPS 的 push/fetch
  大块 POST 会被切断（报 "send-pack: unexpected disconnect"）。
  改用 GitHub Contents API 逐文件 PUT 则稳定可用。

用法：
  python sync_github.py            # 只列出将要变更的文件
  python sync_github.py --apply    # 实际写入 GitHub

凭据：自动从 Git Credential Manager 取 vliantwo 的 token，无需手工填。
"""

import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile

OWNER = "vliantwo"
REPO = "starshack-site"
BRANCH = "main"
GCM = r"C:/Program Files/Git/mingw64/bin/git-credential-manager.exe"

# 不上传的目录/文件
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".workbuddy"}
EXCLUDE_FILES = {".DS_Store"}


def get_token() -> str:
    """从 Git Credential Manager 取出 GitHub token。"""
    inp = "protocol=https\nhost=github.com\n\n"
    out = subprocess.run([GCM, "get"], input=inp, capture_output=True, text=True, timeout=40)
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("无法从 GCM 获取 token，请先在 Git Credential Manager 登录 GitHub 账号")


def api(token: str, method: str, path: str, payload: dict | None = None):
    args = [
        "curl", "-s", "--ssl-no-revoke", "--max-time", "180",
        "-X", method,
        "-H", "Authorization: token " + token,
        "-H", "Accept: application/vnd.github+json",
    ]
    tmp = None
    if payload is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(payload, tmp)
        tmp.close()
        args += ["-d", "@" + tmp.name]
    args.append(f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}")
    r = subprocess.run(args, capture_output=True, text=True)
    if tmp:
        os.unlink(tmp.name)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"_raw": r.stdout[:200]}


def blob_sha(data: bytes) -> str:
    """Git blob 对象的 sha1，用于和 GitHub 返回的 sha 比对。"""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def collect_files():
    """收集本地待同步文件（相对路径）。"""
    root = os.path.dirname(os.path.abspath(__file__))
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if name in EXCLUDE_FILES:
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/")
            result.append(rel)
    return sorted(result)


def main():
    apply_changes = "--apply" in sys.argv
    token = get_token()
    files = collect_files()
    print(f"本地文件 {len(files)} 个，检查远程差异…\n")

    to_create, to_update, unchanged = [], [], []

    for rel in files:
        data = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), rel), "rb").read()
        local = blob_sha(data)
        remote = api(token, "GET", rel + f"?ref={BRANCH}")
        rsha = remote.get("sha") if isinstance(remote, dict) else None

        if rsha is None:
            to_create.append((rel, data))
        elif rsha != local:
            to_update.append((rel, data, rsha))
        else:
            unchanged.append(rel)

    print(f"  新增 {len(to_create)}  修改 {len(to_update)}  无变化 {len(unchanged)}")
    for rel, _ in to_create:
        print("   +", rel)
    for rel, _, _ in to_update:
        print("   ~", rel)
    print()

    if not apply_changes:
        print("（dry-run，加 --apply 才会真正写入 GitHub）")
        return

    for rel, data in to_create:
        r = api(token, "PUT", rel, {
            "message": f"Add {rel}",
            "content": base64.b64encode(data).decode(),
            "branch": BRANCH,
        })
        print("  +", rel, "->", "OK" if r.get("content") else r.get("message", "?"))

    for rel, data, rsha in to_update:
        r = api(token, "PUT", rel, {
            "message": f"Update {rel}",
            "content": base64.b64encode(data).decode(),
            "branch": BRANCH,
            "sha": rsha,
        })
        print("  ~", rel, "->", "OK" if r.get("content") else r.get("message", "?"))

    print("\n同步完成，GitHub Pages 通常 1 分钟内生效：")
    print(f"  https://{OWNER}.github.io/{REPO}/")


if __name__ == "__main__":
    main()
