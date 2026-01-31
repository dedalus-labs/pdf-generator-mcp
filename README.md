# PDF Generator MCP Server

An MCP server that generates PDF and DOCX documents from markdown content.

## Tools

### render_pdf

Generate a PDF document from markdown.

**Parameters:**
- `title` (string): Document title
- `markdown` (string): Markdown content
- `style` (string, optional): "default", "modern", or "minimal"

**Returns:** `{ success, pdf_id, filename, size_bytes, download_url }`

### render_docx

Generate a DOCX document from markdown.

**Parameters:**
- `title` (string): Document title
- `markdown` (string): Markdown content

**Returns:** `{ success, docx_id, filename, size_bytes, download_url }`

## Styles

- **default**: Professional design with blue accents
- **modern**: Clean contemporary design
- **minimal**: Elegant serif typography

## Local Development

### Start the Server

```bash
cd src
uv run python main.py
```

Server runs at `http://127.0.0.1:8080` with:
- MCP endpoint: `/mcp`
- File downloads: `/files/{filename}`

### Test with Client

```bash
cd src
uv run python client.py
```

## Deployment

Deploy to Dedalus Marketplace:

```bash
dedalus mcp deploy
```

## License

MIT
