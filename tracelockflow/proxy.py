# proxy.py
# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp", "rich", "uvicorn"]
# ///

import json
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.middleware.logging import LoggingMiddleware
from starlette.middleware import Middleware as ASGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from os import getenv
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel

console = Console()

DEFAULT_URLS: List[str] = ["https://mcp.deepwiki.com/mcp"]
JUNK_LABELS = {"mcp", "api", "www"}


def parse_urls_from_env() -> List[str]:
    return [u.strip() for u in json.loads(getenv("MCP_SERVER_URLS", "[]")) if isinstance(u, str) and u.strip()] or DEFAULT_URLS

def slug_from_hostname(host: str) -> str:
    all_labels = [l for l in host.split(".") if l]
    labels = [l for l in all_labels if l.lower() not in JUNK_LABELS] or all_labels
    if not labels:
        return "server"
    slug = "-".join(labels).lower()
    slug = "".join(ch if (ch.isalnum() or ch == "-") else "-" for ch in slug).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "server"


def unique_names(urls: List[str]) -> List[Tuple[str, str, str]]:
    prelim: List[Tuple[str, str, str]] = []
    counts: Dict[str, int] = {}
    for url in urls:
        transport = "sse" if url.rstrip("/").endswith("/sse") else "http"
        base = slug_from_hostname(urlparse(url).hostname or "server")
        prelim.append((base, transport, url))
        counts[base] = counts.get(base, 0) + 1
    used: Dict[str, int] = {}
    results: List[Tuple[str, str, str]] = []
    for base, transport, url in prelim:
        name = base if counts[base] == 1 else f"{base}-{transport}"
        n = used.get(name, 0)
        if n:
            name = f"{name}-{n+1}"
        used[name] = used.get(name, 0) + 1
        results.append((name, transport, url))
    return results


def _truncate(value: Any, max_length: int = 800) -> str:
    text = value if isinstance(value, str) else repr(value)
    return text if len(text) <= max_length else text[: max_length - 3] + "..."



def _is_markdown(text: str) -> bool:
    if not isinstance(text, str):
        return False
    if "```" in text or ("[" in text and "](" in text):
        return True
    for line in text.splitlines():
        ls = line.lstrip()
        if ls.startswith(('#', '> ', '- ', '* ')):
            return True
    return False


def _print_json(obj: Any) -> bool:
    try:
        s = json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return False
    console.print(Panel(Syntax(s, "json", word_wrap=True), border_style="grey35"))
    return True


def _print_markdown_limited(text: str, max_lines: int = 10) -> None:
    lines = text.splitlines()
    if len(lines) > max_lines:
        text = "\n".join(lines[:max_lines] + ["..."])
    console.print(Panel(Markdown(text), border_style="grey35"))


def _print_argument_line(name: str, value: Any) -> None:
    console.print("        ", end="")
    console.print(f"[bold yellow]{str(name)}[/bold yellow]=", end="")
    if isinstance(value, (dict, list)):
        try:
            serialized = json.dumps(value, ensure_ascii=False)
        except Exception:
            serialized = repr(value)
    elif isinstance(value, str):
        serialized = value
    else:
        serialized = repr(value)
    console.print(serialized, style="cyan", markup=False)





class ToolTraceMiddleware(Middleware):
    def __init__(self) -> None:
        self.tools_printed = False
        super().__init__()

    async def on_list_tools(self, context: MiddlewareContext, call_next):
        tools = await call_next(context)
        if self.tools_printed:
            return tools

        tool_names_str = ", ".join(getattr(tool, "name", "<tool>") for tool in tools)
        console.print()
        console.print(f"Tools available: {tool_names_str}")
        console.print()

        for tool in tools:
            # Description (if available)
            description = getattr(tool, "description", None)

            # Input schema → properties and simple types
            schema_obj = (
                getattr(tool, "parameters", None)
                or getattr(tool, "input_schema", None)
                or getattr(tool, "inputSchema", None)
            )
            if hasattr(schema_obj, "model_dump"):
                schema_obj = schema_obj.model_dump()
            properties: Dict[str, Any] = (schema_obj.get("properties") if isinstance(schema_obj, dict) else {}) or {}
            required_list = (schema_obj.get("required") if isinstance(schema_obj, dict) else None) or []
            required_set = {str(n) for n in required_list if isinstance(n, str)}

            # Compose argument text; include basic JSON Schema types when present
            def format_entry(argument_name: str) -> str:
                prop_schema = properties.get(argument_name) or {}
                arg_type = prop_schema.get("type")
                if isinstance(arg_type, list):
                    arg_type = "/".join(str(t) for t in arg_type)
                entry = argument_name if not arg_type else f"{argument_name} ({arg_type})"
                desc = prop_schema.get("description")
                if isinstance(desc, str) and desc.strip():
                    entry = f"{entry} — {desc.strip()}"
                return entry

            required_entries: List[str] = [format_entry(n) for n in sorted(properties.keys()) if n in required_set]
            optional_entries: List[str] = [format_entry(n) for n in sorted(properties.keys()) if n not in required_set]

            tool_name = getattr(tool, 'name', '<tool>')
            # Tool name on its own line, bold and colored to match call-site styling
            console.print(f"- [bold magenta]{tool_name}[/bold magenta]")
            # Description (if any) on its own line beneath the tool name
            if description:
                console.print(f"Description:")
                console.print(f"  `{description}`")

            # Arguments grouped below, indented under the tool name
            if required_entries:
                console.print(f"Required arguments: \n  {', \n  '.join(required_entries)}")
            if optional_entries:
                console.print(f"Optional arguments: \n  {', \n  '.join(optional_entries)}")

            # Blank line after each tool block for breathing room
            console.print()
        self.tools_printed = True
        return tools

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        console.rule(style="grey23")
        # Blank line after the rule for readability
        console.print()
        name = getattr(context.message, "name", "<unknown>")
        args = getattr(context.message, "arguments", None) or getattr(
            context.message, "args", None
        )
        if not isinstance(args, dict):
            args = {} if args is None else {"_args": args}

        console.print(f"[cyan]▶ Calling[/] [magenta]{name}[/] [cyan]tool[/] [bold]with arguments:[/]")
        for argument_name in sorted(args.keys()):
            _print_argument_line(argument_name, args[argument_name])

        

        result = await call_next(context)

        data = getattr(result, "data", None)
        content = getattr(result, "content", None)
        if data is not None:
            console.print(f"[green]◀ [/][bold magenta]{name}[/bold magenta][green] tool result data:[/]")
            if not _print_json(data):
                if isinstance(data, str) and _is_markdown(data):
                    _print_markdown_limited(data)
                else:
                    console.print(_truncate(data, 2000))
            console.rule(style="grey23")
        elif content:
            first = content[0] if isinstance(content, list) and content else content
            text = getattr(first, "text", None)
            if text is None:
                text = first
            console.print(f"[green]◀ [/][bold magenta]{name}[/bold magenta][green] tool result content:[/]")
            if isinstance(text, (dict, list)) and _print_json(text):
                pass
            elif isinstance(text, str) and _is_markdown(text):
                _print_markdown_limited(text)
            else:
                console.print(_truncate(text, 2000))
            console.rule(style="grey23")
        else:
            console.print(f"[green]◀ [/][bold magenta]{name}[/bold magenta][green] tool result:[/]")
            console.print(_truncate(result, 2000))
            console.rule(style="grey23")
        return result


def start_intercept_proxy() -> None:
    upstream_urls = parse_urls_from_env()
    server_entries = unique_names(upstream_urls)
    proxy_config = {
        "mcpServers": {
            name: {"url": url, "transport": transport}
            for name, transport, url in server_entries
        }
    }

    console.print()
    console.print("[bold]MCP upstreams:[/bold]")
    for server_name, server_transport, server_url in server_entries:
        console.print(f"  [bold green]{server_name:22s}[/] -> [cyan]{server_url}[/]  [dim][{server_transport}][/dim]")
    console.print()

    proxy = FastMCP.as_proxy(proxy_config, name="multi-mcp-proxy")
    proxy.add_middleware(LoggingMiddleware(include_payloads=True, max_payload_length=2000))

    port = int(getenv("PORT", "8084"))
    base_url = f"http://127.0.0.1:{port}/mcp"
    console.print(f"[bold]Local Streamable HTTP endpoint:[/bold] [cyan]{base_url}[/]")
    console.print()

    proxy.add_middleware(ToolTraceMiddleware())

    middleware = [
        ASGIMiddleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=False,
        )
    ]

    proxy.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        middleware=middleware,
        show_banner=False
    )


if __name__ == "__main__":
    try:
        start_intercept_proxy()
    except KeyboardInterrupt:
        sys.exit(0)