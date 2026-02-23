# Mermaid MCP Server

> 基于 Model Context Protocol (MCP) 的 Mermaid 图表转换服务器，为 AI 客户端提供强大的图表生成能力

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![MCP](https://img.shields.io/badge/mcp-1.9+-green.svg)
![UV](https://img.shields.io/badge/uv-latest-purple.svg)

---

## 项目介绍

Mermaid MCP Server 是一个专业的基于 Model Context Protocol (MCP) 的 Mermaid 图表转换服务器，为 AI 客户端提供强大的图表生成能力。该项目能够将 Mermaid 图表代码转换为多种格式的图像文件（PNG、JPG、SVG、PDF），让用户能够在支持 MCP 协议的各种 AI 客户端中轻松生成高质量的图表。

### 核心特性

- **多格式输出**: 支持 PNG、JPG、SVG、PDF 等多种图像格式
- **主题定制**: 内置 default、dark、neutral、forest 四种精美主题
- **自定义选项**: 支持背景颜色、图像尺寸等参数自定义
- **语法验证**: 提供实时的 Mermaid 语法验证功能
- **示例资源**: 内置丰富的图表类型示例代码
- **错误处理**: 完善的错误处理机制和友好的错误提示
- **STDIO/SSE 双模式**: 支持 STDIO 和 SSE 两种通信模式
- **uv 包管理**: 使用超快的 uv 包管理器

---

## 功能清单

| 功能名称 | 功能说明 | 技术栈 | 状态 |
|---------|---------|--------|------|
| 图表转换 | Mermaid 代码转图像 | mermaid.ink API | ✅ 稳定 |
| 多格式输出 | PNG/JPG/SVG/PDF | requests + base64 | ✅ 稳定 |
| 主题定制 | 4种内置主题 | mermaid.ink | ✅ 稳定 |
| 语法验证 | 实时语法检查 | mermaid-cli | ✅ 稳定 |
| 示例资源 | 丰富图表示例 | 静态资源 | ✅ 稳定 |
| 错误处理 | 完善错误提示 | Python 异常处理 | ✅ 稳定 |
| MCP 协议 | Model Context Protocol | mcp[cli] | ✅ 稳定 |
| SSE 模式 | Server-Sent Events | FastAPI + Uvicorn | ✅ 稳定 |

---

## 技术架构

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 主要开发语言 |
| MCP | 1.9+ | Model Context Protocol |
| FastAPI | 0.104+ | Web 框架（SSE 模式） |
| Uvicorn | 0.24+ | ASGI 服务器 |
| requests | 2.31+ | HTTP 客户端 |
| uv | latest | Python 包管理器 |

### 通信架构

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            通信架构图                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌──────────────────┐       ┌─────────────────────────┐       ┌─────────────┐ │
│   │  AI 客户端         │ ◄────► │   Mermaid MCP Server    │ ◄────► │ Mermaid API │ │
│   │ (Cursor/Claude)   │       │   STDIO/SSE             │       │  mermaid.ink│ │
│   └──────────────────┘       └─────────────────────────┘       └─────────────┘ │
│           │                            │                              │        │
│           ▼                            ▼                              ▼        │
│   AI 对话界面                MCP 协议通信              图表渲染转换      │
│   生成图表请求                双向数据传输              返回图像数据     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 安装说明

### 环境要求

- Python 3.12+
- uv 包管理器（推荐）

### 安装依赖

**方式一：使用 uv 安装（推荐）**

```bash
# 克隆仓库
git clone https://github.com/wwwzhouhui/mermaid_mcp_server.git
cd mermaid_mcp_server

# 安装依赖
uv sync
```

**方式二：使用 pip 安装**

```bash
pip install -r requirements.txt
```

---

## 使用说明

### 客户端配置

#### Cursor 配置

在 `~/.cursor/mcp.json` 文件中添加以下配置：

**STDIO 模式（推荐）**：

```json
{
  "mcpServers": {
    "mermaid-mcp-server-png-pdf-jpg-svg": {
      "command": "uvx",
      "args": [
        "mermaid-mcp-server-png-pdf-jpg-svg"
      ]
    }
  }
}
```

**SSE 模式**：

```json
{
  "mcpServers": {
    "mermaid-mcp-server-png-pdf-jpg-svg": {
      "url": "http://127.0.0.1:8003/sse"
    }
  }
}
```

#### Cherry Studio 配置

1. 打开 Cherry Studio
2. 进入 **设置 → MCP Servers → 添加服务器**
3. 配置参数：
   - **名称**: `mermaid-mcp-server-png-pdf-jpg-svg`
   - **描述**: `Mermaid 图表生成服务`
   - **类型**: `STDIO`
   - **命令**: `uvx`
   - **参数**: `mermaid-mcp-server-png-pdf-jpg-svg`
4. 点击保存并启用

![Cherry Studio 配置示例](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1753102609763.png)

#### Claude Desktop 配置

在 `claude_desktop_config.json` 文件中添加：

```json
{
  "mcpServers": {
    "mermaid-mcp-server-png-pdf-jpg-svg": {
      "command": "uvx",
      "args": [
        "mermaid-mcp-server-png-pdf-jpg-svg"
      ]
    }
  }
}
```

#### Continue.dev 配置

在 `config.json` 文件中添加：

```json
{
  "mcpServers": {
    "mermaid-mcp-server-png-pdf-jpg-svg": {
      "command": "uvx",
      "args": [
        "mermaid-mcp-server-png-pdf-jpg-svg"
      ]
    }
  }
}
```

### 启动服务

#### STDIO 模式（推荐用于桌面客户端）

```bash
uv run python main.py
```

#### SSE 模式（用于网络连接）

```bash
uv run python main.py --sse
```

---

## 配置说明

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `HOST` | 服务器地址 | `0.0.0.0` |
| `PORT` | 服务器端口 | `8003` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `MERMAID_API_BASE_URL` | Mermaid API 地址 | `https://mermaid.ink` |
| `REQUEST_TIMEOUT` | 请求超时时间（秒） | `30` |
| `DEBUG` | 调试模式 | `false` |
| `DEVELOPMENT_MODE` | 开发模式 | `false` |

---

## 可用工具

### 1. convert_mermaid_to_image

将 Mermaid 图表代码转换为多种格式的图像文件

**参数**：
- `mermaid_code` (string): Mermaid 图表代码
- `output_format` (string, 可选): 输出格式，支持 png、jpg、svg、pdf，默认 "png"
- `theme` (string, 可选): 主题样式，支持 default、dark、neutral、forest，默认 "default"
- `background_color` (string, 可选): 背景颜色，十六进制代码
- `width` (number, 可选): 图像宽度（像素）
- `height` (number, 可选): 图像高度（像素）

**支持的输出格式**: PNG、JPG、SVG、PDF

### 2. validate_mermaid_syntax

验证 Mermaid 图表代码的语法正确性

**参数**：
- `mermaid_code` (string): 需要验证的 Mermaid 图表代码

**返回结果**:
- `valid` (boolean): 是否验证通过
- `error_message` (string): 错误信息（如果验证失败）

### 3. get_supported_options

获取转换器支持的选项

**返回结果**:
- `themes` (array): 支持的主题列表
- `formats` (array): 支持的格式列表

---

## 支持的图表类型

- **流程图 (Flowchart)**: 用于表示流程和算法
- **时序图 (Sequence Diagram)**: 用于表示对象之间的交互
- **甘特图 (Gantt Chart)**: 用于项目进度管理
- **饼图 (Pie Chart)**: 用于表示数据占比
- **Git 图 (Git Graph)**: 用于表示 Git 提交历史
- **思维导图 (Mind Map)**: 用于表示知识结构
- **类图 (Class Diagram)**: 用于表示类结构

---

## 使用示例

### 流程图示例

```
请使用 convert_mermaid_to_image 工具生成一个流程图：
flowchart TD
    A[开始] --> B{判断条件}
    B -->|是| C[执行动作1]
    B -->|否| D[执行动作2]
    C --> E[结束]
    D --> E
```

### 时序图示例

```
请使用 convert_mermaid_to_image 工具生成一个时序图，使用深色主题：
sequenceDiagram
    participant 用户
    participant 系统
    participant 数据库

    用户->>系统: 登录请求
    系统->>数据库: 验证用户
    数据库-->>系统: 返回结果
    系统-->>用户: 登录成功
```

### 语法验证示例

```
首先使用 validate_mermaid_syntax 验证语法，然后使用 convert_mermaid_to_image 生成图表
```

---

## 资源示例

### 获取图表示例

可以通过以下资源 URI 获取不同类型的图表示例：

- `mermaid://examples/flowchart` - 流程图示例
- `mermaid://examples/sequence` - 时序图示例
- `mermaid://examples/gantt` - 甘特图示例
- `mermaid://examples/pie` - 饼图示例
- `mermaid://examples/gitgraph` - Git 图示例
- `mermaid://examples/mindmap` - 思维导图示例
- `mermaid://examples/class` - 类图示例

---

## 项目结构

```
mermaid_mcp_server/
├── mermaid_mcp_server/       # 核心模块
│   ├── __init__.py
│   └── main.py             # 主程序入口
├── requirements.txt          # 依赖列表（pip）
├── pyproject.toml           # 项目配置（uv）
├── .env.example            # 环境变量示例
├── README.md               # 项目文档
└── .vscode/                # VSCode 配置
    └── settings.json
```

---

## 开发指南

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/wwwzhouhui/mermaid_mcp_server.git
cd mermaid_mcp_server

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env

# 启动服务（STDIO 模式）
uv run python main.py

# 启动服务（SSE 模式）
uv run python main.py --sse
```

### 调试模式

启用详细日志输出：

```bash
export LOG_LEVEL=DEBUG
uv run python main.py
```

---

## 常见问题

<details>
<summary>Q: 网络连接问题？</summary>

A:
1. 检查网络连接和防火墙设置
2. 确认 mermaid.ink API 可访问
3. 检查代理设置
</details>

<details>
<summary>Q: 语法错误？</summary>

A:
1. 使用 validate_mermaid_syntax 工具检查语法
2. 参考 Mermaid 官方文档
3. 使用示例资源中的代码
</details>

<details>
<summary>Q: 图表过大？</summary>

A:
1. 简化图表内容
2. 分割为多个小图表
3. 调整图像尺寸参数
</details>

<details>
<summary>Q: uvx 命令未找到？</summary>

A:
1. 安装 uv 包管理器：`curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 或使用 pip 全局安装包
3. 检查 PATH 环境变量
</details>

<details>
<summary>Q: SSE 模式无法连接？</summary>

A:
1. 确认服务已以 SSE 模式启动
2. 检查端口 8003 是否被占用
3. 确认 URL 配置正确
</details>

<details>
<summary>Q: 生成的图像质量差？</summary>

A:
1. 增加图像尺寸参数
2. 选择合适的主题
3. 优化 Mermaid 代码结构
</details>

<details>
<summary>Q: 转换超时？</summary>

A:
1. 检查网络连接速度
2. 增加 REQUEST_TIMEOUT 环境变量
3. 简化图表复杂度
</details>

<details>
<summary>Q: 主题不生效？</summary>

A:
1. 确认主题名称拼写正确
2. 检查是否支持该主题
3. 尝试使用不同的主题名称
</details>

<details>
<summary>Q: 如何自定义背景颜色？</summary>

A:
1. 使用 background_color 参数
2. 格式为十六进制颜色代码（如 #FFFFFF）
3. 仅支持部分输出格式
</details>

---

## 技术交流群

欢迎加入技术交流群，分享你的使用心得和反馈建议：

![技术交流群](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/%25E5%25BE%25AE%25E4%25BF%25A1%25E5%259B%25BE%25E7%2589%2587_20260223133201_158_292.jpg)

---

## 作者联系

- **微信**: laohaibao2025
- **邮箱**: 75271002@qq.com

![微信二维码](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Screenshot_20260123_095617_com.tencent.mm.jpg)

---

## 打赏

如果这个项目对你有帮助，欢迎请我喝杯咖啡 ☕

**微信支付**

![微信支付](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250914152855543.png)

---

## Star History

如果觉得项目不错，欢迎点个 Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=wwwzhouhui/mermaid_mcp_server&type=Date)](https://star-history.com/#wwwzhouhui/mcp_mcp_server&Date)

---

## License

MIT License

---

## 更新日志

### v0.1.0 (当前版本)

- ✅ 初始版本发布
- ✅ 支持 PNG、JPG、SVG、PDF 多格式输出
- ✅ 集成四种主题样式（default、dark、neutral、forest）
- ✅ 提供语法验证和示例资源功能
- ✅ 支持 STDIO 和 SSE 双模式通信

### v0.0.3 (2025-07-21)

- ✅ 初始版本发布
- ✅ 支持多格式图表转换
- ✅ 语法验证功能
- ✅ 示例资源功能

---

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

---

## 注意事项

- 图表生成可能需要几秒钟时间，请耐心等待
- 确保网络连接正常，服务依赖 mermaid.ink 在线 API
- 生成的图像数据以 base64 格式返回
- 复杂图表可能需要更长的生成时间

---

**Enjoy creating beautiful diagrams with Mermaid! 🎨✨**
