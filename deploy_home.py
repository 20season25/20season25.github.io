#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 D:\\CODE\\home 同步到服务器 /var/www/home（首页 + /breath 等子目录）。

用法: python deploy_home.py
复用 leancoach 的 SSH 工具与密钥。只写 /var/www/home 前缀。
"""
import importlib.util
import os
import posixpath

HERE = os.path.dirname(os.path.abspath(__file__))
REMOTE_ROOT = "/var/www/home"
SSHTOOL = r"D:\CODE\leancoach\deploy\server-sshtool.py"
SKIP = {".git", ".gitignore", "deploy_home.py", "README.md", "__pycache__", "deploy"}

spec = importlib.util.spec_from_file_location("sshtool", SSHTOOL)
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

cli = s.connect()
sftp = cli.open_sftp()


def mkdirs(remote):
    cur = ""
    for part in remote.strip("/").split("/"):
        cur += "/" + part
        try:
            sftp.stat(cur)
        except FileNotFoundError:
            sftp.mkdir(cur)


n = 0
for base, dirs, files in os.walk(HERE):
    dirs[:] = [d for d in dirs if d not in SKIP]
    rel = os.path.relpath(base, HERE).replace("\\", "/")
    rdir = REMOTE_ROOT if rel == "." else posixpath.join(REMOTE_ROOT, rel)
    mkdirs(rdir)
    for fn in files:
        if fn in SKIP:
            continue
        sftp.put(os.path.join(base, fn), posixpath.join(rdir, fn))
        print("put", posixpath.join(rdir, fn))
        n += 1

sftp.close()
cli.close()
print(f"\n完成：{n} 个文件 → {REMOTE_ROOT}")
