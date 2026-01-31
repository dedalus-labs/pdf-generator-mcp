# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

"""Sample MCP client for testing the PDF Generator MCP server."""

import asyncio

from dedalus_mcp import MCPClient


SERVER_URL = "http://localhost:8080/mcp"


async def main() -> None:
    client = await MCPClient.connect(SERVER_URL)

    # List tools
    result = await client.list_tools()
    print(f"\nAvailable tools ({len(result.tools)}):\n")
    for t in result.tools:
        print(f"  {t.name}")
        if t.description:
            print(f"    {t.description[:80]}...")
        print()

    # Test render_pdf
    print("--- render_pdf ---")
    pdf_result = await client.call_tool(
        "render_pdf",
        {
            "title": "Project Proposal",
            "markdown": """
## Executive Summary

This proposal outlines our approach to delivering a comprehensive website redesign.

## Scope of Work

- Discovery and research phase
- UX/UI design
- Frontend development
- Backend integration
- Quality assurance and testing

## Timeline

| Phase | Duration |
|-------|----------|
| Discovery | 2 weeks |
| Design | 3 weeks |
| Development | 4 weeks |
| Testing | 1 week |

## Investment

**Total Project Cost: $15,000**

- 50% due upon project kickoff
- 50% due upon completion
            """,
            "style": "modern",
        },
    )
    print(pdf_result)
    print()

    # Test render_docx
    print("--- render_docx ---")
    docx_result = await client.call_tool(
        "render_docx",
        {
            "title": "Meeting Notes",
            "markdown": """
## Attendees

- John Smith
- Jane Doe
- Bob Johnson

## Discussion Points

1. Q4 budget review
2. Product roadmap updates
3. Team expansion plans

## Action Items

- John to prepare budget report by Friday
- Jane to schedule follow-up meeting
- Bob to draft hiring plan
            """,
        },
    )
    print(docx_result)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
