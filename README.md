# Mermaid MCP Server

## 项目简介

Mermaid MCP Server 是一个基于 Model Context Protocol (MCP) 的 Mermaid 图表转换服务器，为AI客户端提供强大的图表生成能力。该项目的开发初衷是为了提供一个强大的图表生成服务，能够将 Mermaid 图表代码转换为多种格式的图像文件，让用户能够在支持MCP协议的各种AI客户端中轻松生成高质量的图表。

**核心功能特性：**

- **多格式输出**：支持 PNG、JPG、SVG、PDF 等多种图像格式
- **主题定制**：内置 default、dark、neutral、forest 四种精美主题
- **自定义选项**：支持背景颜色、图像尺寸等参数自定义
- **语法验证**：提供实时的 Mermaid 语法验证功能
- **示例资源**：内置丰富的图表类型示例代码
- **错误处理**：完善的错误处理机制和友好的错误提示

**支持的图表类型：**

- 流程图（Flowchart）
- 时序图（Sequence Diagram）
- 甘特图（Gantt Chart）
- 饼图（Pie Chart）
- Git图（Git Graph）
- 思维导图（Mind Map）
- 类图（Class Diagram）


## 部署指南

### **环境依赖**

- Python >= 3.12
- UV 包管理器（推荐）


### **安装方式**

**方式一：使用UV安装（推荐）**

```bash
# 克隆仓库
git clone https://github.com/wwwzhouhui/mermaid_mcp_server.git
cd mermaid_mcp_server

# 安装依赖
uv sync
```

**方式二：使用pip安装**

```bash
pip install -r requirements.txt
```


### **客户端配置**

#### **Cursor配置**

在 `~/.cursor/mcp.json` 文件中添加以下配置：

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

sse配置

{
  "mcpServers": {
    "mermaid-mcp-server-png-pdf-jpg-svg": {
      "url": "http://127.0.0.1:8003/sse"
    }
  }
}

#### **Cherry Studio配置**

1. 打开 Cherry Studio

2. 进入 **设置 → MCP Servers → 添加服务器**

3. 配置参数：
   - **名称**: `mermaid-mcp-server-png-pdf-jpg-svg`
   - **描述**: `Mermaid图表生成服务`
   - **类型**: `STDIO`
   - **命令**: `uvx`
   - **参数**: `mermaid-mcp-server-png-pdf-jpg-svg
   
4. 点击保存并启用

   详细图解

   ![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1753102609763.png)

![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1753102786420.png)

#### **Claude Desktop配置**

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


#### **Continue.dev配置**

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


### **启动服务**

#### **STDIO模式（推荐用于桌面客户端）**
```bash
uv run python main.py
```


## 可用工具

### **1. convert_mermaid_to_image**

将 Mermaid 图表代码转换为多种格式的图像文件

- `mermaid_code` (string): Mermaid 图表代码
- `output_format` (string, 可选): 输出格式，支持 png、jpg、svg、pdf，默认"png"
- `theme` (string, 可选): 主题样式，支持 default、dark、neutral、forest，默认"default"
- `background_color` (string, 可选): 背景颜色，十六进制代码
- `width` (number, 可选): 图像宽度（像素）
- `height` (number, 可选): 图像高度（像素）

**支持的输出格式**: PNG、JPG、SVG、PDF

### **2. validate_mermaid_syntax**

验证 Mermaid 图表代码的语法正确性

- `mermaid_code` (string): 需要验证的 Mermaid 图表代码

**返回结果**:
- `valid` (boolean): 是否验证通过
- `error_message` (string): 错误信息（如果验证失败）

### **3. get_supported_options**

获取转换器支持的选项

**返回结果**:
- `themes` (array): 支持的主题列表
- `formats` (array): 支持的格式列表


## 使用示例

### **流程图示例**

```
请使用convert_mermaid_to_image工具生成一个流程图：
flowchart TD
    A[开始] --> B{判断条件}
    B -->|是| C[执行动作1]
    B -->|否| D[执行动作2]
    C --> E[结束]
    D --> E
```

![image-20250721102017442](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250721102017442.png)

### **时序图示例**

```
请使用convert_mermaid_to_image工具生成一个时序图，使用深色主题：
sequenceDiagram
    participant 用户
    participant 系统
    participant 数据库
    
    用户->>系统: 登录请求
    系统->>数据库: 验证用户
    数据库-->>系统: 返回结果
    系统-->>用户: 登录成功
```

生成的PDF 

![image-20250721161147623](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250721161147623.png)

### **语法验证示例**

```
首先使用validate_mermaid_syntax验证语法，然后使用convert_mermaid_to_image生成图表
```


## 资源示例

### **获取图表示例**

可以通过以下资源URI获取不同类型的图表示例：

- `mermaid://examples/flowchart` - 流程图示例
- `mermaid://examples/sequence` - 时序图示例  
- `mermaid://examples/gantt` - 甘特图示例
- `mermaid://examples/pie` - 饼图示例
- `mermaid://examples/gitgraph` - Git图示例
- `mermaid://examples/mindmap` - 思维导图示例
- `mermaid://examples/class` - 类图示例


## 注意事项

- 图表生成可能需要几秒钟时间，请耐心等待
- 确保网络连接正常，服务依赖mermaid.ink在线API
- 生成的图像数据以base64格式返回
- 复杂图表可能需要更长的生成时间


## 故障排除

### **常见问题**

1. **网络连接问题**: 检查网络连接和防火墙设置
2. **语法错误**: 使用validate_mermaid_syntax工具检查语法
3. **图表过大**: 简化图表内容或分割为多个小图表

### **调试模式**

启用详细日志输出：

```bash
export LOG_LEVEL=DEBUG
uv run python main.py
```

## 更新说明

2025年7月21日-version 0.0.3：初始版本发布，支持多格式图表转换、语法验证、示例资源功能。

## 项目信息

**许可证**: MIT License

**作者**: wwzhouhui - [75271002@qq.com](mailto:75271002@qq.com)

**版本**: v0.1.0

- 初始版本发布
- 支持PNG、JPG、SVG、PDF多格式输出
- 集成四种主题样式
- 提供语法验证和示例资源功能

**贡献**: 欢迎提交Issue和Pull Request来改进这个项目


## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=wwwzhouhui/mcp-mermaid-server&type=Date)](https://star-history.com/#prompt-engineering/mcp-mermaid-server&Date)