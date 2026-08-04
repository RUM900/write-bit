"""解析 PDF 招标文件，输出 Markdown 到 stdout。"""
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("请先安装: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("用法: python parse_pdf.py <招标文件.pdf>", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
if not Path(file_path).exists():
    print(f"文件不存在: {file_path}", file=sys.stderr)
    sys.exit(1)

content = []
with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            content.append(text)

        tables = page.extract_tables()
        for table in tables:
            rows = []
            for i, row in enumerate(table):
                cells = [str(c) if c else '' for c in row]
                rows.append('| ' + ' | '.join(cells) + ' |')
                if i == 0 and len(table) > 1:
                    cols = len(row)
                    rows.append('|' + '|'.join(['---'] * cols) + '|')
            content.extend(rows)
            content.append('')

markdown = '\n'.join(content)
print(markdown)