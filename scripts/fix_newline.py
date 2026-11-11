# -*- coding: utf-8 -*-
"""修复 index.html 里 JS 字符串中的真实换行符（join("\n") 模式）。"""
import io
import re

p = r"D:\CODE\home\index.html"
s = io.open(p, encoding="utf-8").read()

# 1) 已知精确坏点
n1 = s.count('print(out.join("\n"));')
s = s.replace('print(out.join("\n"));', 'print(out.join("\\n"));')

# 2) 通用：join("<真实换行>") → join("\n")
s, n2 = re.subn(r'join\("\n"\)', 'join("\\\\n")', s)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print(f"fixed: exact={n1}, regex={n2}")
