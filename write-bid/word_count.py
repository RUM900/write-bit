"""
字数统计工具 - 正确统计中文字数（解决 Windows 下 wc -m 统计错误的问题）
用法: python word_count.py <文件路径>
"""
import sys, re
from pathlib import Path

if len(sys.argv) < 2:
    print("用法: python word_count.py <文件路径>", file=sys.stderr)
    sys.exit(1)

path = Path(sys.argv[1])
if not path.exists():
    print(f"文件不存在: {path}", file=sys.stderr)
    sys.exit(1)

text = path.read_text(encoding='utf-8')

# 总字符数（含标点、空格、Markdown 语法符号）
total_chars = len(text)

# 纯中文字符数（只统计汉字）
chinese_chars = len(re.findall(r'[一-鿿]', text))

# 去掉 Markdown 语法符号后的实际内容字数
# 去掉标题标记、加粗标记、表格分隔线、列表标记等
clean = text
clean = re.sub(r'^#{1,6}\s+', '', clean, flags=re.MULTILINE)  # 去掉标题 #
clean = re.sub(r'\*\*(.*?)\*\*', r'\1', clean)  # 去掉加粗
clean = re.sub(r'^\|[-:| ]+\|$', '', clean, flags=re.MULTILINE)  # 去掉表格分隔行
clean = re.sub(r'^[-*]\s+', '', clean, flags=re.MULTILINE)  # 去掉列表标记
clean = re.sub(r'^\d+[.、]\s+', '', clean, flags=re.MULTILINE)  # 去掉数字列表标记
clean = re.sub(r'^\s*[-*_]{3,}\s*$', '', clean, flags=re.MULTILINE)  # 去掉分隔线
clean = re.sub(r'[|:]', '', clean)  # 去掉表格线
clean = re.sub(r'\s+', '', clean)  # 去掉空白字符

# 按章节统计
sections = {}
current = '前言'
s_lines = []
for line in text.split('\n'):
    m = re.match(r'^##\s+(\d+\.?\s*.*)', line)
    if m:
        if s_lines:
            sections[current] = ''.join(s_lines)
        current = m.group(1).strip()
        s_lines = [line]
    else:
        s_lines.append(line)
if s_lines:
    sections[current] = ''.join(s_lines)

print(f"文件: {path.name}")
print(f"{'='*50}")
print(f"总字符数（含语法符号）: {total_chars}")
print(f"纯中文字符数: {chinese_chars}")
print(f"实际内容字数（去语法符号）: {len(clean)}")
print(f"估算页数（按800字/页）: {len(clean)/800:.0f} 页")
print(f"{'='*50}")
print(f"章节字数分布:")
for s, content in sections.items():
    # 去掉该章节的 Markdown 语法
    cc = content
    cc = re.sub(r'^#{1,6}\s+', '', cc, flags=re.MULTILINE)
    cc = re.sub(r'\*\*(.*?)\*\*', r'\1', cc)
    cc = re.sub(r'^\|[-:| ]+\|$', '', cc, flags=re.MULTILINE)
    cc = re.sub(r'^[-*]\s+', '', cc, flags=re.MULTILINE)
    cc = re.sub(r'[|:]', '', cc)
    cc = re.sub(r'\s+', '', cc)
    print(f"  {len(cc):>6}字 | {s[:50]}")

print(f"{'='*50}")
print(f"目标: 96,000字 (120页)")
if len(clean) >= 96000:
    print(f"状态: [达标]（超出 {len(clean) - 96000} 字）")
else:
    print(f"状态: [不足]（还差 {96000 - len(clean)} 字）")