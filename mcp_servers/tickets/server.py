from mcp.server import MCPServer

from mcp_servers.tickets.tools import register_tools


mcp = MCPServer(
    "OpsPilot Tickets",
    instructions=(
        "Provides incident ticket creation and lookup "
        "for the simulated operations environment."
    ),
)


register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")