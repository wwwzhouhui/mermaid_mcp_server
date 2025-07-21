#!/usr/bin/env python3
"""
MCP Mermaid Server 测试客户端
用于测试 MCP 服务器的功能
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """测试 MCP 服务器功能"""
    
    # 创建服务器参数
    server_params = StdioServerParameters(
        command="python3",
        args=["main.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()
            
            print("🚀 MCP Mermaid Server 测试开始")
            print("=" * 50)
            
            # 测试 1: 获取可用工具
            print("\n📋 测试 1: 获取可用工具")
            tools = await session.list_tools()
            print(f"可用工具数量: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 测试 2: 获取可用资源
            print("\n📋 测试 2: 获取可用资源")
            resources = await session.list_resources()
            print(f"可用资源数量: {len(resources.resources)}")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # 测试 3: 语法验证
            print("\n🔍 测试 3: Mermaid 语法验证")
            test_code = """
            flowchart TD
                A[Start] --> B{Decision}
                B -->|Yes| C[Action 1]
                B -->|No| D[Action 2]
                C --> E[End]
                D --> E
            """
            
            validation_result = await session.call_tool(
                "validate_mermaid_syntax",
                {"mermaid_code": test_code}
            )
            print(f"验证结果: {json.dumps(validation_result.content[0].text, indent=2, ensure_ascii=False)}")
            
            # 测试 4: 图表转换
            print("\n🎨 测试 4: Mermaid 图表转换")
            conversion_result = await session.call_tool(
                "convert_mermaid_to_image",
                {
                    "mermaid_code": test_code,
                    "output_format": "png",
                    "theme": "dark",
                    "width": 800,
                    "height": 600
                }
            )
            
            result_data = json.loads(conversion_result.content[0].text)
            if result_data.get("success"):
                print("✅ 转换成功!")
                data = result_data["data"]
                print(f"  - 格式: {data['format']}")
                print(f"  - 主题: {data['theme']}")
                print(f"  - 文件大小: {data['size_bytes']} 字节")
                print(f"  - MIME 类型: {data['mime_type']}")
                print(f"  - Base64 数据长度: {len(data['image_base64'])} 字符")
            else:
                print(f"❌ 转换失败: {result_data.get('error')}")
            
            # 测试 5: 获取示例资源
            print("\n📖 测试 5: 获取示例资源")
            example_resource = await session.read_resource("mermaid://examples/sequence")
            print("序列图示例:")
            print(example_resource.contents[0].text[:200] + "...")
            
            # 测试 6: 错误处理
            print("\n⚠️  测试 6: 错误处理")
            error_result = await session.call_tool(
                "convert_mermaid_to_image",
                {
                    "mermaid_code": "",  # 空代码应该返回错误
                    "output_format": "png"
                }
            )
             # 测试 7: 获取支持的选项
            print("\n🔧 测试 7: 获取支持的选项")
            options_result = await session.call_tool("get_supported_options", {})
            
            options_data = json.loads(options_result.content[0].text)
            print("服务器支持以下选项:")
            print(f"  - 主题 (Themes): {', '.join(options_data['themes'])}")
            print(f"  - 格式 (Formats): {', '.join(options_data['formats'])}")

            print("\n" + "=" * 50)
            print("🎉 所有测试完成!") # 修改这里的结束语
            
            error_data = json.loads(error_result.content[0].text)
            if not error_data.get("success"):
                print(f"✅ 错误处理正常: {error_data.get('error')}")
            else:
                print("❌ 错误处理异常")
            
            print("\n" + "=" * 50)
            print("🎉 测试完成!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())