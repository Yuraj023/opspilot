from mcp.server import MCPServer

from mcp_servers.deployment.tools import register_tools


mcp = MCPServer(
    "OpsPilot Deployment",
    instructions=(
        "Provides deployment history and safe remediation planning "
        "information. Production-changing actions are not directly "
        "executed by this server."
    ),
)


register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")