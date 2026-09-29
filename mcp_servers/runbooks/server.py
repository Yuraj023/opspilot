from mcp.server import MCPServer

from mcp_servers.runbooks.tools import register_tools


mcp = MCPServer(
    "OpsPilot Runbooks",
    instructions=(
        "Provides operational runbooks and incident-response "
        "procedures."
    ),
)


register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")