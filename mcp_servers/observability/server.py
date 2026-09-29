from mcp.server import MCPServer

from mcp_servers.observability.tools import register_tools


mcp = MCPServer(
    "OpsPilot Observability",
    instructions=(
        "Provides read-only observability information such as "
        "logs, metrics, alerts, and service health."
    ),
)


register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")