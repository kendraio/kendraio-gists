// We use Formly to show forms in Kendraio App. Formly currently (23rd January 2025) lacks
// support for resolving JSON schemas that have external references.
// This script merges together the referenced JSON schemas using `@apidevtools/json-schema-ref-parser`
// The output can then be used in the config of a Kendraio Form block's JSON schema property.

// It does so for this example URL:
const schemaUrl = "https://test-library.murmurations.network/v2/schemas/people_schema-v0.1.0";

// Usage:
// I was able to run this script like so, on a GitHub Codespace with Ubuntu 20.04.6 LTS,
// with the following bash terminal commands:
`
curl -fsSL https://bun.sh/install | bash # for macOS, Linux, and WSL
~/.bun/bin/bun install @apidevtools/json-schema-ref-parser
~/.bun/bin/bun run schema_merge_tool.ts > merged_schema.json
`

import $RefParser from "@apidevtools/json-schema-ref-parser";

try {
  const resolvedSchema = await new $RefParser().dereference(schemaUrl);
  console.log(JSON.stringify(resolvedSchema, null, 2));
} catch (error) {
  console.error("An error occurred:", error);
}