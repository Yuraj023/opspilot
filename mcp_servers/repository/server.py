from mcp.server import MCPServer

from mcp_servers.repository.tools import register_tools


mcp = MCPServer(
    "OpsPilot Repository",
    instructions=(
        "Provides read-only source-code and repository information "
        "for incident investigation."
    ),
)


register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")