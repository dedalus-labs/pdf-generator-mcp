# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

"""Entry point for PDF Generator MCP server."""

import asyncio

from dotenv import load_dotenv


load_dotenv()

from server import main


if __name__ == "__main__":
    asyncio.run(main())
