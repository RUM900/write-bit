# write-bid 技能使用说明

投标方案写作助手。解析招标文件，规划大纲，逐节生成技术方案。

## 安装

本技能内置解析脚本，只需安装基础依赖：

```bash
# 解析 DOCX 文件
pip install python-docx

# 如需解析 PDF 文件
pip install pdfplumber
```

## 安装技能文件

### Claude Code

将 `write-bid` 文件夹复制到：

```
Windows: C:\Users\<用户名>\.claude\skills\write-bid\
Mac/Linux: ~/.claude/skills/write-bid/
```

### 其他 Agent 工具

将 `SKILL.md` 中的提示词内容复制到你的 agent 配置中。

## 使用方法

```
/write-bid 招标文件.docx
```

或

```
/write-bid 招标文件.pdf
```

## 工作流程

1. 解析招标文件（DOCX/PDF → Markdown）
2. 分析评分项、废标条款、采购清单
3. 选择章节骨架（可调整）
4. 规划章节子节
5. 逐节写作
6. 检查评分覆盖

## 输出

完整的 Markdown 格式技术方案，可直接使用或导出 Word。

## 注意事项

- 不确定的信息用 `【待补充】` 标记，不编造数据
- 根据项目类型调整章节骨架
- 每节完成后可修改再继续