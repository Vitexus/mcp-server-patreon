import argparse
import os
from importlib.metadata import PackageNotFoundError, version

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def _version() -> str:
    try:
        return version("patreon-mcp-server")
    except PackageNotFoundError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(
        prog="mcp-server-patreon",
        description="MCP server for the Patreon API (campaigns, members, posts).",
        epilog="Environment: PATREON_ACCESS_TOKEN (required), TRANSPORT (default: stdio).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {_version()}")
    parser.parse_args()

    # Imported after argument parsing: the Patreon client is created at import
    # time and requires PATREON_ACCESS_TOKEN, which --help/--version must not.
    from patreon_mcp_server.mcp_server import mcp
    import patreon_mcp_server.tools  # noqa: F401  - registers tools on mcp

    mcp.run(transport=os.getenv("TRANSPORT", "stdio"))


if __name__ == "__main__":
    main()
