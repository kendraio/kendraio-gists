 # TraceLockFlow

Reliable results from unreliable inputs?

Learning how Model Context Protocol agents use existing services from MCP servers, to make fixed (static) workflows from Large Language Models log traces, with human control.

We can learn from the most capable tool using LLMs use the rapidly expanding range of MCP servers and existing service interfaces.

```bash
# Clone this repository and navigate to this README.md file's folder:
git clone https://github.com/kendraio/kendraio-gists.git
cd kendraio-gists/tracelockflow
# Install Astral UV
curl -LsSf https://astral.sh/uv/install.sh | sh
# Run the intercept proxy in one terminal:
uv run proxy.sh
```

In another terminal run this after:
```bash
# Run the OpenAPI server for the Flow to use:
MCPO_LOG_LEVEL=DEBUG uvx mcpo --port 8044 --server-type streamable-http  --cors-allow-origins="*" -- https://mcp.deepwiki.com/mcp
```
The static workflow with no LLM magic (when used):
Open up https://app.kendra.io/mcpProxy/deepWiki