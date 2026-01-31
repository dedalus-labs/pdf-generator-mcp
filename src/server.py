# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

"""PDF Generator MCP Server with file serving endpoint."""

import asyncio
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route

from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings

from pdf import pdf_tools, FILES_DIR


# --- Server ------------------------------------------------------------------

server = MCPServer(
    name="pdf-generator-mcp",
    http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    streamable_http_stateless=True,
)


# --- File Serving Routes -----------------------------------------------------

async def serve_file(request):
    """Serve generated PDF/DOCX files."""
    filename = request.path_params["filename"]
    filepath = FILES_DIR / filename

    if not filepath.exists():
        return JSONResponse({"error": "File not found"}, status_code=404)

    # Determine content type
    if filename.endswith(".pdf"):
        media_type = "application/pdf"
    elif filename.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        media_type = "application/octet-stream"

    return FileResponse(
        filepath,
        media_type=media_type,
        filename=filename,
    )


async def list_files(request):
    """List all generated files."""
    files = []
    for f in FILES_DIR.iterdir():
        if f.is_file() and (f.suffix == ".pdf" or f.suffix == ".docx"):
            files.append({
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "created": f.stat().st_ctime,
            })
    return JSONResponse({"files": files})


# --- Main --------------------------------------------------------------------

async def run_file_server():
    """Run the file serving endpoint."""
    import uvicorn

    file_routes = [
        Route("/files/{filename:path}", serve_file, methods=["GET"]),
        Route("/files", list_files, methods=["GET"]),
    ]
    file_app = Starlette(routes=file_routes)

    config = uvicorn.Config(file_app, host="127.0.0.1", port=8081, log_level="warning")
    file_server = uvicorn.Server(config)
    await file_server.serve()


async def main() -> None:
    """Start the MCP server and file server concurrently."""
    server.collect(*pdf_tools)

    # Run both servers concurrently
    await asyncio.gather(
        server.serve(port=8080),
        run_file_server(),
    )
