@echo off
echo ========================================
echo write-bid 技能安装脚本
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

:: 安装依赖
echo [1/3] 安装依赖包...
pip install python-docx pdfplumber
if errorlevel 1 (
    echo [警告] 部分依赖安装失败，但可继续
)

:: 创建技能目录
echo [2/3] 安装技能文件...
set SKILL_DIR=%USERPROFILE%\.claude\skills\write-bid
if not exist "%SKILL_DIR%" mkdir "%SKILL_DIR%"

copy /Y write-bid\SKILL.md "%SKILL_DIR%\" >nul
if errorlevel 1 (
    echo [错误] 技能文件复制失败
    pause
    exit /b 1
)

:: 复制解析脚本
echo [3/3] 安装解析脚本...
copy /Y write-bid\*.py "%SKILL_DIR%\" >nul

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用方法：
echo   1. 重启 Claude Code
echo   2. 输入: /write-bid 招标文件.docx
echo.
pause