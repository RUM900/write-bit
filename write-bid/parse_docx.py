"""解析 DOCX 招标文件，输出 Markdown 到 stdout。"""
import sys
from pathlib import Path

try:
    import docx
except ImportError:
    print("请先安装: pip install python-docx", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("用法: python parse_docx.py <招标文件.docx>", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
if not Path(file_path).exists():
    print(f"文件不存在: {file_path}", file=sys.stderr)
    sys.exit(1)

from docx.text.paragraph import Paragraph
from docx.table import Table

doc = docx.Document(file_path)

content = []
for element in doc.element.body:
    tag = element.tag.split('}')[-1]  # 去掉命名空间

    if tag == 'p':
        para = Paragraph(element, doc)
        text = para.text.strip()
        if not text:
            continue
        style = para.style.name
        if style.startswith('Heading') or '标题' in style:
            level = 2 if '2' in style else 1 if '1' in style else 3
            content.append(f"{'#' * level} {text}")
        else:
            content.append(text)

    elif tag == 'tbl':
        table = Table(element, doc)
        rows = []
        for i, row in enumerate(table.rows):
            cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
            rows.append('| ' + ' | '.join(cells) + ' |')
            if i == 0 and len(table.rows) > 1:
                cols = len(row.cells)
                rows.append('|' + '|'.join(['---'] * cols) + '|')
        content.extend(rows)
        content.append('')

markdown = '\n'.join(content)
print(markdown)