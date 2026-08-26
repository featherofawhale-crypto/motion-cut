#!/usr/bin/env python3
"""Small stdio MCP client used to drive the local Premiere Pro MCP server."""

from __future__ import annotations

import argparse
import anyio
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Override via env PR_MCP_SERVER if your install path differs.
SERVER_SCRIPT = os.environ.get(
    "PR_MCP_SERVER",
    os.path.expanduser("~/.local/lib/node_modules/adobe-premiere-pro-mcp/dist/index.js"),
)


async def run(tool: str | None, arguments: dict[str, object], list_tools: bool) -> None:
    env = dict(os.environ)
    env["PREMIERE_TEMP_DIR"] = "/tmp/premiere-mcp-bridge"
    server = StdioServerParameters(
        command="node",
        args=[SERVER_SCRIPT],
        env=env,
    )
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools() if list_tools else await session.call_tool(tool, arguments)
            print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tool", nargs="?")
    parser.add_argument("arguments", nargs="?", default="{}")
    parser.add_argument("--list-tools", action="store_true")
    args = parser.parse_args()
    if not args.list_tools and not args.tool:
        parser.error("tool is required unless --list-tools is used")
    raw_arguments = args.arguments
    if raw_arguments.startswith("@"):
        raw_arguments = Path(raw_arguments[1:]).read_text(encoding="utf-8")
    anyio.run(run, args.tool, json.loads(raw_arguments), args.list_tools)


if __name__ == "__main__":
    main()
