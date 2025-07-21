import base64
import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 MCP 服务器
mcp = FastMCP("Mermaid Converter")

@mcp.tool()
def convert_mermaid_to_image(
    mermaid_code: str,
    output_format: str = "png",
    theme: str = "default",
    background_color: str = "",
    width: Optional[int] = None,
    height: Optional[int] = None
) -> Dict[str, Any]:
    """
    将 Mermaid 图表代码转换为多种格式的图像（PNG、JPG、PDF、SVG）。
    
    参数:
        mermaid_code: 要转换的 Mermaid 图表语法代码
        output_format: 输出格式 - png、jpg、svg 或 pdf（默认：png）
        theme: 视觉主题 - default、dark、neutral 或 forest（默认：default）
        background_color: 背景颜色，十六进制代码（如 FF0000）或带 ! 前缀的命名颜色（如 !white）
        width: 图像宽度（像素，可选）
        height: 图像高度（像素，可选）
    
    返回:
        包含转换后图像数据和元数据的字典
    """
    try:
        # 验证输入参数
        if not mermaid_code or not mermaid_code.strip():
            return {
                "success": False,
                "error": "Mermaid 代码是必需的，不能为空"
            }
        
        # 清理 Mermaid 代码（移除 markdown 代码块标记）
        cleaned_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
        
        # 验证输出格式
        valid_formats = ["png", "jpg", "jpeg", "svg", "pdf"]
        output_format = output_format.lower()
        if output_format not in valid_formats:
            return {
                "success": False,
                "error": f"无效的输出格式 '{output_format}'。支持的格式：{', '.join(valid_formats)}"
            }
        
        # 验证主题
        valid_themes = ["default", "dark", "neutral", "forest"]
        if theme not in valid_themes:
            return {
                "success": False,
                "error": f"无效的主题 '{theme}'。支持的主题：{', '.join(valid_themes)}"
            }
        
        logger.info(f"Converting Mermaid diagram to {output_format} format with theme {theme}")
        
        # Base64 编码 Mermaid 代码
        try:
            encoded_diagram = base64.urlsafe_b64encode(cleaned_code.encode('utf-8')).decode('ascii')
        except Exception as e:
            return {
                "success": False,
                "error": f"编码图表失败：{str(e)}"
            }
        
        # 构建 API URL
        url = _build_api_url(encoded_diagram, output_format, theme, background_color, width, height)
        
        logger.info(f"Making request to {url}")
        
        # 发送 HTTP 请求
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                if response.status_code == 400:
                    error_msg = f"无效的 Mermaid 语法：{response.text}"
                elif response.status_code == 413:
                    error_msg = "图表对于 API 来说太大了"
                else:
                    error_msg = f"转换失败：HTTP {response.status_code}"
                
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }
            
            # 确定 MIME 类型
            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg", 
                "jpeg": "image/jpeg",
                "svg": "image/svg+xml",
                "pdf": "application/pdf"
            }
            
            mime_type = mime_types.get(output_format, "image/png")
            filename = f"mermaid_diagram.{output_format}"
            
            # 将图像数据编码为 base64 以便传输
            image_base64 = base64.b64encode(response.content).decode('ascii')
            
            logger.info(f"Successfully converted diagram to {output_format} ({len(response.content)} bytes)")
            
            return {
                "success": True,
                "data": {
                    "image_base64": image_base64,
                    "mime_type": mime_type,
                    "filename": filename,
                    "size_bytes": len(response.content),
                    "format": output_format,
                    "theme": theme
                }
            }
            
        except requests.Timeout:
            error_msg = "转换超时 - mermaid.ink 响应时间过长"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
        except requests.ConnectionError:
            error_msg = "连接错误：无法访问 mermaid.ink 服务"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
        except Exception as e:
            error_msg = f"请求错误：{str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
    except Exception as e:
        error_msg = f"转换过程中发生意外错误：{str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def _build_api_url(
    encoded_diagram: str, 
    output_format: str, 
    theme: str, 
    background_color: str, 
    width: Optional[int] = None, 
    height: Optional[int] = None
) -> str:
    """
    构建 mermaid.ink API URL
    
    Args:
        encoded_diagram: Base64 编码的 mermaid 代码
        output_format: 目标格式 (png/jpg/svg/pdf)
        theme: 视觉主题
        background_color: 背景颜色
        width: 图像宽度
        height: 图像高度
        
    Returns:
        完整的 API URL
    """
    # 根据格式选择不同的端点
    if output_format == "svg":
        base_url = f"https://mermaid.ink/svg/{encoded_diagram}"
    elif output_format == "pdf":
        base_url = f"https://mermaid.ink/pdf/{encoded_diagram}"
    else:  # png, jpg, jpeg
        base_url = f"https://mermaid.ink/img/{encoded_diagram}"
    
    # 构建查询参数
    params = {}
    
    # 格式特定参数
    if output_format in ["png", "jpg", "jpeg"]:
        params["type"] = output_format
        
    # 主题参数（仅适用于图像格式，不适用于 SVG/PDF）
    if theme and theme != "default" and output_format in ["png", "jpg", "jpeg"]:
        params["theme"] = theme
    
    # 背景颜色参数
    if background_color:
        # 支持十六进制颜色 (FF0000) 和命名颜色 (!white)
        if background_color.startswith("!"):
            params["bgColor"] = background_color
        else:
            # 移除 # 符号并验证是否为有效的十六进制颜色
            color = background_color.lstrip("#")
            if len(color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in color):
                params["bgColor"] = color
    
    # 尺寸参数
    if width:
        params["width"] = str(width)
    if height:
        params["height"] = str(height)
    
    # 组合 URL 和参数
    if params:
        return f"{base_url}?{urlencode(params)}"
    else:
        return base_url

@mcp.tool()
def validate_mermaid_syntax(mermaid_code: str) -> Dict[str, Any]:
    """
    通过尝试简单转换来验证 Mermaid 图表语法。
    
    参数:
        mermaid_code: 要验证的 Mermaid 图表语法代码
    
    返回:
        包含验证结果的字典
    """
    try:
        if not mermaid_code or not mermaid_code.strip():
            return {
                "valid": False,
                "error": "Mermaid 代码是必需的，不能为空"
            }
        
        # 清理代码
        cleaned_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
        
        # 尝试编码
        try:
            encoded_diagram = base64.urlsafe_b64encode(cleaned_code.encode('utf-8')).decode('ascii')
        except Exception as e:
            return {
                "valid": False,
                "error": f"编码图表失败：{str(e)}"
            }
        
        # 使用 SVG 格式进行快速验证（通常最快）
        url = f"https://mermaid.ink/svg/{encoded_diagram}"
        
        try:
            response = requests.head(url, timeout=10)  # 使用 HEAD 请求更快
            
            if response.status_code == 200:
                return {
                    "valid": True,
                    "message": "Mermaid 语法有效"
                }
            elif response.status_code == 400:
                return {
                    "valid": False,
                    "error": "无效的 Mermaid 语法"
                }
            else:
                return {
                    "valid": False,
                    "error": f"验证失败：HTTP {response.status_code}"
                }
                
        except requests.Timeout:
            return {
                "valid": False,
                "error": "验证超时"
            }
        except requests.ConnectionError:
            return {
                "valid": False,
                "error": "连接错误：无法访问验证服务"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"验证错误：{str(e)}"
            }
            
    except Exception as e:
        return {
            "valid": False,
            "error": f"验证过程中发生意外错误：{str(e)}"
        }

@mcp.resource("mermaid://examples/{diagram_type}")
def get_mermaid_example(diagram_type: str) -> str:
    """
    获取不同图表类型的 Mermaid 代码示例。
    
    参数:
        diagram_type: 图表类型（flowchart、sequence、gantt、pie 等）
    
    返回:
        指定图表类型的 Mermaid 代码示例
    """
    examples = {
        "flowchart": """
flowchart TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
        """.strip(),
        
        "sequence": """
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
        """.strip(),
        
        "gantt": """
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task      : 24d
        """.strip(),
        
        "pie": """
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15
        """.strip(),
        
        "gitgraph": """
gitgraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    commit
        """.strip(),
        
        "mindmap": """
mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
        """.strip(),
        
        "class": """
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    class Cat {
        +String color
        +meow()
    }
    Animal <|-- Dog
    Animal <|-- Cat
        """.strip()
    }
    
    if diagram_type.lower() in examples:
        return examples[diagram_type.lower()]
    else:
        available_types = ", ".join(examples.keys())
        return f"未知的图表类型 '{diagram_type}'。可用类型：{available_types}"

@mcp.tool()
def get_supported_options() -> Dict[str, Any]:
    """
    获取转换器支持的选项，如图表主题和输出格式。
    
    返回:
        一个包含支持的主题和格式列表的字典。
    """
    logger.info("Providing list of supported options.")
    return {
        "themes": ["default", "dark", "neutral", "forest"],
        "formats": ["png", "jpg", "svg", "pdf"]
    }

if __name__ == "__main__":
    # 配置 MCP 服务器设置
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8003
    
    # 启动 MCP 服务器（SSE 模式）
    mcp.run(transport="sse")