#!/bin/bash
echo "========================================"
echo "write-bid 技能安装脚本"
echo "========================================"
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

# 安装依赖
echo "[1/3] 安装依赖包..."
pip3 install python-docx pdfplumber
if [ $? -ne 0 ]; then
    echo "[警告] 部分依赖安装失败，但可继续"
fi

# 创建技能目录
echo "[2/3] 安装技能文件..."
SKILL_DIR="$HOME/.claude/skills/write-bid"
mkdir -p "$SKILL_DIR"

# 复制技能文件
cp write-bid/SKILL.md "$SKILL_DIR/"
if [ $? -ne 0 ]; then
    echo "[错误] 技能文件复制失败"
    exit 1
fi

echo
echo "========================================"
echo "安装完成！"
echo "========================================"
echo
echo "使用方法："
echo "  1. 重启 Claude Code"
echo "  2. 输入: /write-bid 招标文件.docx"