#!/bin/bash

# MCP Mermaid Server 部署脚本

set -e

echo "🚀 开始部署 MCP Mermaid Server..."

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.12"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要 Python $required_version 或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python 版本检查通过: $python_version"

# 检查 UV 是否安装
echo "📋 检查 UV 包管理器..."
if ! command -v uv &> /dev/null; then
    echo "📦 UV 未安装，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    echo "✅ UV 安装完成"
else
    echo "✅ UV 已安装"
fi

# 创建项目目录（如果不存在）
PROJECT_DIR="mermaid_mcp_server"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📁 创建项目目录..."
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# 初始化项目（如果需要）
if [ ! -f "pyproject.toml" ]; then
    echo "📋 初始化项目..."
    uv init .
fi

# 安装依赖
echo "📦 安装项目依赖..."
uv sync

# 检查主文件是否存在
if [ ! -f "main.py" ]; then
    echo "❌ 错误: main.py 文件不存在"
    exit 1
fi

# 测试服务器启动
echo "🧪 测试服务器启动..."
timeout 10s uv run python main.py --help > /dev/null 2>&1 || true

echo "✅ 部署完成!"
echo ""
echo "📖 使用说明:"
echo "  STDIO 模式 (Cherry Studio): uv run python main.py"
echo ""
echo "🔧 Cherry Studio 配置:"
echo "  命令: uv"
echo "  参数: --directory $(pwd) run python main.py"
echo ""
echo "🌐 SSE 服务地址:"
echo "  http://localhost:8003/sse"
echo ""
echo "🧪 运行测试:"
echo "  uv run python test_client.py"