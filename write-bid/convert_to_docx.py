"""将 Markdown 技术方案转换为 Word 文档。"""
import sys
from pathlib import Path
import re

try:
    import docx
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
except ImportError as e:
    print(f"请先安装: pip install python-docx （{e}）", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("用法: python convert_to_docx.py <方案.md> [输出文件.docx]", file=sys.stderr)
    sys.exit(1)

md_path = Path(sys.argv[1])
if not md_path.exists():
    print(f"文件不存在: {md_path}", file=sys.stderr)
    sys.exit(1)

out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else md_path.with_suffix('.docx')


def set_font(run, name='宋体', size=12, bold=False, color=None):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading(doc, text, level):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    set_font(run, '黑体', {1: 18, 2: 15, 3: 13}.get(level, 12), bold=True)
    return h


def add_table(doc, md_table_lines):
    """将 Markdown 表格行转换为 Word 表格。"""
    rows = [line for line in md_table_lines if line.strip() and not re.match(r'^\|[-:| ]+\|$', line)]
    if not rows:
        return
    data = [row.strip().strip('|').split('|') for row in rows]
    data = [[c.strip() for c in row] for row in data]

    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.style = 'Table Grid'
    for i, row_data in enumerate(data):
        for j, cell_text in enumerate(row_data):
            if j < len(table.columns):
                cell = table.cell(i, j)
                cell.text = cell_text
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(10.5)
    doc.add_paragraph()


doc = Document()

# 设置默认样式
style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

md = md_path.read_text(encoding='utf-8')
lines = md.split('\n')

i = 0
while i < len(lines):
    line = lines[i].strip()

    if not line:
        i += 1
        continue

    # 标题
    m = re.match(r'^(#{1,3})\s+(.*)', line)
    if m:
        level = len(m.group(1))
        text = m.group(2).strip()
        add_heading(doc, text, level)
        i += 1
        continue

    # 表格
    if line.startswith('|') and line.endswith('|'):
        table_lines = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            table_lines.append(lines[i])
            i += 1
        add_table(doc, table_lines)
        continue

    # 普通段落
    para = doc.add_paragraph()
    run = para.add_run(line)
    set_font(run, size=12)
    i += 1

doc.save(str(out_path))
print(f"已导出: {out_path}")