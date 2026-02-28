import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_playwright_client():
    # Windows needs 'npx.cmd' to execute correctly through standard IO
    server_params = StdioServerParameters(
        command="npx.cmd", 
        args=["-y", "@modelcontextprotocol/server-playwright"],
        env=None
    )

    print("🚀 Connecting to Playwright MCP Server...")

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # This is where your previous error occurred
                await session.initialize()
                print("✅ Connected successfully!")

                # List tools to verify it's working
                tools_response = await session.list_tools()
                print(f"\nFound {len(tools_response.tools)} tools:")
                for tool in tools_response.tools:
                    print(f" - {tool.name}")
                    
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(run_playwright_client())