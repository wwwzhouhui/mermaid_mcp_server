@echo off
chcp 65001 >nul
REM Installation Script

echo Checking Python environment...
python --version || echo Please install Python 3.12 or higher && exit /b 1

echo Installing dependencies...
pip install -e .

IF %ERRORLEVEL% NEQ 0 (
    echo Installation failed, try running as administrator...
    echo Please right-click this script and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo Installation successful!
echo.
echo Usage:
echo 1. Command line: mermaid-mcp-server-png-pdf-jpg-svg
echo 2. Or run directly: python main.py
echo.
echo Advanced options:
echo - Use SSE mode: mermaid-mcp-server-png-pdf-jpg-svg --transport sse
echo - Debug mode: mermaid-mcp-server-png-pdf-jpg-svg --debug
echo - Custom port: mermaid-mcp-server-png-pdf-jpg-svg --transport sse --port 8080
echo.
pause