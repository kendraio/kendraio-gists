In a chat with the Large Language Model named Gemini 2.0 Pro Experimental 02-05 ("gemini-2.0-pro-exp-02-05"), I (Luke), used https://gitingest.com on the MIT licensed https://github.com/APIDevTools/json-schema-ref-parser repo and asked for an analysis of Node.js dependencies, and explanation of Node.js dependencies that it relies on.

I also asked for a new, minimal browser-native, JSON-only schema dereferencer with a "middleware" system to allow changing the HTTP requests to add CORS proxy support in a single, self-contained code block with no external dependencies, with no YAML.
I got this, untested snippet of ~180 lines of code:

```javascript
class JSONSchemaRefParser {
  constructor() {
    this.cache = new Map();
  }

  async dereference(schemaOrURL, options = {}) {
    const { middleware = this.defaultMiddleware, baseUrl = null } = options;

    const schema = typeof schemaOrURL === 'string' ?
      await this.fetchSchema(schemaOrURL, middleware) :
      schemaOrURL;

      const resolvedBaseUrl = baseUrl || (typeof schemaOrURL === 'string' ? schemaOrURL : window.location.href);

    return this.resolveRefs(schema, resolvedBaseUrl, new Set(), middleware);
  }

  async fetchSchema(url, middleware) {
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    const initialRequest = { url, method: 'GET' };
    const middlewareResult = await middleware(initialRequest);

    if (middlewareResult && middlewareResult.parsed) {
      // Middleware provided a parsed result, so bypass fetching
      this.cache.set(url, middlewareResult.parsed);
      return middlewareResult.parsed;
    }

    const request = (middlewareResult && middlewareResult.request) || initialRequest;
    const response = await fetch(request.url, request);

    if (!response.ok) {
      throw new Error(`Failed to fetch ${request.url}: ${response.status} ${response.statusText}`);
    }

    const text = await response.text();
    const parsed = this.parseContent(text, request.url);
    this.cache.set(url, parsed);
    return parsed;
  }

  parseContent(text, url) {
    try {
      return JSON.parse(text);
    } catch (error) {
      throw new Error(`Error parsing JSON in ${url}: ${error.message}`);
    }
  }

  async resolveRefs(schema, baseUrl, seen, middleware) {
    if (typeof schema !== 'object' || schema === null) {
      return schema;
    }

    if (seen.has(schema)) {
      return schema; // Prevent infinite recursion on circular refs
    }
    seen.add(schema);

    if (Array.isArray(schema)) {
      const resolvedArray = [];
      for (const item of schema) {
        resolvedArray.push(await this.resolveRefs(item, baseUrl, seen, middleware));
      }
      return resolvedArray;
    }

    if (schema.$ref && typeof schema.$ref === 'string') {
      const [refUrl, refPointer] = schema.$ref.split('#');
      const fullRefUrl = refUrl ? new URL(refUrl, baseUrl).href : baseUrl;
      let resolvedSchema = await this.fetchSchema(fullRefUrl, middleware);

      if (refPointer) {
        resolvedSchema = this.resolvePointer(resolvedSchema, refPointer);
      }

      if (Object.keys(schema).length > 1) {
        const cloned = { ...resolvedSchema };
        for (const key in schema) {
          if (key !== '$ref') {
            cloned[key] = schema[key];
          }
        }
        return this.resolveRefs(cloned, baseUrl, seen, middleware); // resolve the merged object
      }

      return this.resolveRefs(resolvedSchema, fullRefUrl, seen, middleware); // Recursively resolve
    }

    const resolvedObject = {};
    for (const key in schema) {
      resolvedObject[key] = await this.resolveRefs(schema[key], baseUrl, seen, middleware);
    }
    return resolvedObject;
  }

  resolvePointer(schema, pointer) {
    if (!pointer) {
      return schema;
    }
    const parts = pointer.substring(1).split('/').map(part =>
      part.replace(/~1/g, '/').replace(/~0/g, '~')
    );
    let current = schema;
    for (const part of parts) {
      if (current && typeof current === 'object' && Object.hasOwn(current, part)) {
        current = current[part];
      } else {
        throw new Error(`Invalid JSON pointer "${pointer}" in schema ${JSON.stringify(schema)}`);
      }
    }
    return current;
  }

  defaultMiddleware(request) {
    // Default middleware: Does nothing, just returns the original request.
    return { request };
  }
}

// --- Example Usage ---

async function runExample() {
    // Example with custom middleware (add a header):
    const addHeaderMiddleware = (request) => {
      const modifiedRequest = {
        ...request,
        headers: {
          ...request.headers,
          'X-Custom-Header': 'MyValue',
        },
      };
      return { request: modifiedRequest };
    };

    const parserWithMiddleware = new JSONSchemaRefParser();
    try {
        const schema = await parserWithMiddleware.dereference('my-schema.json', { middleware: addHeaderMiddleware });
        console.log('Dereferenced with middleware:', schema);
    }
    catch(err) {
        console.error(err);
    }

    // Example with a proxy (bypass fetch entirely):
    const proxyMiddleware = (request) => {
        if(request.url.startsWith('http://example.com')) {
            // Instead of fetching, return a pre-parsed object:
            return { parsed: { data: 'Proxied data for ' + request.url } };
        }
        return {request}; // Pass-through

    }
    const parserWithProxy = new JSONSchemaRefParser();

    try {
        const schema2 = await parserWithProxy.dereference('http://example.com/schema.json', { middleware: proxyMiddleware });
        console.log('Dereferenced with proxy:', schema2);
    }
    catch(err) {
        console.error(err);
    }
}

// In an HTML file, you would include:
// <script>
//   // ... (paste the JSONSchemaRefParser class code here) ...
// </script>

// Run the example (you'll need to have a local server running to avoid CORS issues when fetching local files)
runExample();

```
