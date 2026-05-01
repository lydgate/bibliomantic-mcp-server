#!/usr/bin/env python3
"""
Bibliomantic MCP Server — HTTP transport

Run this for remote access (claude.ai, Poke, etc.).
The stdio entry point (bibliomantic_fastmcp.py) remains for Claude Desktop / openclaw.

Required env:
  MCP_API_KEY   — Bearer token clients must send; server exits if unset.

Optional env:
  HTTP_HOST     — bind address (default 127.0.0.1, use 0.0.0.0 behind a proxy)
  HTTP_PORT     — port (default 3001)
"""

import logging
import os
import sys

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

try:
    from enhanced_divination import EnhancedBiblioManticDiviner
    from enhanced_iching_core import IChingAdapter
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from enhanced_divination import EnhancedBiblioManticDiviner
    from enhanced_iching_core import IChingAdapter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# --- Auth -------------------------------------------------------------------

API_KEY = os.environ.get("MCP_API_KEY", "").strip()
if not API_KEY:
    logger.error("MCP_API_KEY is not set. Set it before starting the HTTP server.")
    sys.exit(1)

HOST = os.environ.get("HTTP_HOST", "127.0.0.1")
PORT = int(os.environ.get("HTTP_PORT", "3001"))

# --- MCP server (same tools as stdio entry point) ---------------------------

from typing import Optional  # noqa: E402 (after path fix)

mcp = FastMCP(name="Bibliomantic Oracle", dependencies=["secrets"])

diviner = EnhancedBiblioManticDiviner()
iching = IChingAdapter()


@mcp.tool()
def i_ching_divination(query: Optional[str] = None) -> str:
    """Perform I Ching divination using traditional three-coin method."""
    result = diviner.perform_simple_divination()
    if not result["success"]:
        return f"Divination failed: {result.get('error', 'Unknown error')}"

    response = (
        f"🎋 **I Ching Divination**\n\n"
        f"**Hexagram {result['hexagram_number']}: {result['hexagram_name']}**\n\n"
        f"{result['interpretation']}\n\n"
        f"*Generated using traditional three-coin method with cryptographically secure randomness.*"
    )
    if result.get("changing_lines"):
        response += f"\n\n**Changing Lines:** {', '.join(map(str, result['changing_lines']))}"
    if query:
        response += f"\n\n**Your Question:** {query}"
        response += "\n\n**Guidance:** Consider how this hexagram's wisdom applies to your specific situation."
    return response


@mcp.tool()
def bibliomantic_consultation(query: str) -> str:
    """Perform bibliomantic consultation following Philip K. Dick's approach."""
    if not query.strip():
        return "Please provide a question for bibliomantic consultation."

    augmented_query, divination_info = diviner.divine_query_augmentation(query)
    if "error" in divination_info:
        return f"Consultation failed: {divination_info['error']}"

    return (
        f"🔮 **Bibliomantic Consultation**\n\n"
        f"**Your Question:** {query}\n\n"
        f"**Oracle's Guidance — Hexagram {divination_info['hexagram_number']}: {divination_info['hexagram_name']}**\n\n"
        f"{divination_info['interpretation']}\n\n"
        f"**Bibliomantic Integration:**\n"
        f"The I Ching suggests considering this wisdom in the context of your question.\n\n"
        f"*Method: Traditional three-coin divination · Philip K. Dick's bibliomantic approach*"
    )


@mcp.tool()
def get_hexagram_details(hexagram_number: int) -> str:
    """Get detailed information about a specific I Ching hexagram (1-64)."""
    if not isinstance(hexagram_number, int) or not (1 <= hexagram_number <= 64):
        return "Please provide a valid hexagram number between 1 and 64."
    name, interpretation = iching.get_hexagram_by_number(hexagram_number)
    return (
        f"📖 **Hexagram {hexagram_number}: {name}**\n\n"
        f"**Traditional Interpretation:**\n{interpretation}"
    )


@mcp.tool()
def server_statistics() -> str:
    """Get bibliomantic server statistics and system information."""
    stats = diviner.get_divination_statistics()
    return (
        f"📊 **Bibliomantic Server Statistics**\n\n"
        f"**System Status:** {stats['system_status'].title()}\n"
        f"**Total Hexagrams:** {stats['total_hexagrams']}\n"
        f"**Divination Method:** {stats['divination_method']}\n"
        f"**Transport:** HTTP (streamable-http)\n"
        f"**Bind:** {HOST}:{PORT}"
    )


# --- Auth middleware ---------------------------------------------------------

UNAUTHENTICATED_PATHS = {"/health"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in UNAUTHENTICATED_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("authorization", "")
        api_key_header = request.headers.get("x-api-key", "")

        token = ""
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
        elif api_key_header:
            token = api_key_header.strip()

        if token != API_KEY:
            logger.warning("Rejected unauthenticated request to %s", request.url.path)
            return JSONResponse(
                {"jsonrpc": "2.0", "error": {"code": -32001, "message": "Unauthorized"}, "id": None},
                status_code=401,
            )
        return await call_next(request)


# --- Health endpoint --------------------------------------------------------

async def health(request: Request) -> Response:
    return JSONResponse({"status": "ok", "service": "bibliomantic-mcp"})


# --- App assembly -----------------------------------------------------------

mcp_app = mcp.streamable_http_app()

app = Starlette(
    routes=[
        Route("/health", health),
        Mount("/", app=mcp_app),
    ]
)
app.add_middleware(ApiKeyMiddleware)


# --- Entry point ------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Bibliomantic HTTP MCP server on %s:%d", HOST, PORT)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
