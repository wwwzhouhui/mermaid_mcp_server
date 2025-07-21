#!/bin/bash
# 安装脚本

echo "正在检查 Python 环境..."
python3 --version || { echo "请安装 Python 3.12 或更高版本"; exit 1; }

echo "正在安装依赖..."
pip install -e .

if [ $? -ne 0 ]; then
    echo "安装失败，尝试使用管理员权限..."
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

echo ""
echo "安装成功！"
echo ""
echo "使用方法："
echo "1. 命令行运行：mermaid-mcp-server-png-pdf-jpg-svg"
echo "2. 或者直接运行：python main.py"
echo ""
echo "高级选项："
echo "- 使用 SSE 模式：mermaid-mcp-server-png-pdf-jpg-svg --transport sse"
echo "- 调试模式：mermaid-mcp-server-png-pdf-jpg-svg --debug"
echo "- 自定义端口：mermaid-mcp-server-png-pdf-jpg-svg --transport sse --port 8080"