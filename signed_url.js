// Creates authentication headers for AWS S3 or Backblaze B2 API requests
// Uses AWS Signature Version 4 specification
// Example usage: Listing all available buckets and contents of a specific bucket
// Add applicationKey and keyID to the config object to use with Backblaze B2

async function makeSignedRequestHeaders(config) {
  // Creates a AWS Signature Version 4 signed request
  // Intended for AWS S3 API or Backblaze B2 API
  const {
    secretKey,
    accessKeyId,
    region,
    bucket,
    endpoint = "s3.amazonaws.com", // Sensible default
    service = "s3",
    method = "GET",
  } = config;

  // Calculates hash of a string for signing steps
  async function sha256String(data) {
    const digest = await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(data)
    );
    return Array.from(new Uint8Array(digest))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  // Uses HMAC with SHA-256 to sign data with a given key during key derivation
  async function hmac(key, data) {
    const cryptoKey = await crypto.subtle.importKey(
      "raw",
      typeof key === "string" ? new TextEncoder().encode(key) : key,
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"]
    );
    return crypto.subtle.sign(
      "HMAC",
      cryptoKey,
      new TextEncoder().encode(data)
    );
  }

  // Declare the AWS signature algorithm we're conforming to
  const ALGO = "AWS4-HMAC-SHA256";

  // Format dates for AWS requirements:
  const dateDelimiterRemover = /[:-]|\..*$/g;
  // The x-amz-date header needs uses this date format:
  const date = new Date().toISOString().replace(dateDelimiterRemover, "") + "Z";
  // The signed URL uses the shorter date format:
  const shortDate = date.slice(0, 8); // Cut off time and timezone

  // The first request in a session has an empty body
  const emptyStringDigest = await sha256String("");

  const host = bucket ? `${bucket}.${endpoint}` : endpoint;
  // Build credential scope string used in both signature calculation and final header
  const scope = `${shortDate}/${region}/${service}/aws4_request`;
  // Build the "canonical request" that includes HTTP method, path, and headers
  // This gets hashed and used in the final signature calculation
  // Create canonical request string - this is what actually gets signed
  const canonicalRequest = [
    method,
    "/",
    "",
    `host:${host}`,
    `x-amz-date:${date}`,
    "",
    "host;x-amz-date",
    emptyStringDigest,
  ].join("\n");

  const hashedCanonicalRequest = await sha256String(canonicalRequest);
  // Create the string to sign according to AWS specifications
  const stringToSign = [ALGO, date, scope, hashedCanonicalRequest].join("\n");

  // Each part of the key derivation process is signed with the secret key and hash in a chain
  // Each step adds another component to the key derivation making it stronger
  const kDate = await hmac(`AWS4${secretKey}`, shortDate);
  const kRegion = await hmac(kDate, region);
  const kService = await hmac(kRegion, service);
  const kSigning = await hmac(kService, "aws4_request");

  // Calculate signature
  const signature = Array.from(
    new Uint8Array(await hmac(kSigning, stringToSign))
  )
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  // Put the final "Authorization" header together:
  const credentials = `Credential=${accessKeyId}/${scope}`;
  const signedHeaders = "SignedHeaders=host;x-amz-date";
  const signatureValue = `Signature=${signature}`;
  const authValue = `${ALGO} ${credentials}, ${signedHeaders}, ${signatureValue}`;
  // Return the AWS Signature V4 request signed headers
  return {
    Host: host,
    "X-Amz-Date": date,
    Authorization: authValue,
  };
}

async function constructSignedRequest(config, path = "/") {
  // Combines URL and signed headers into a ready-to-use request object
  // Works with both AWS S3 and Backblaze B2 APIs
  // Assemble URL and headers to make an signed request
  const protocol = config.protocol || "https";
  const host = config.bucket
    ? `${config.bucket}.${config.endpoint}`
    : config.endpoint;
  const url = `${protocol}://${host}${path}`;
  const headers = await makeSignedRequestHeaders(config);

  return {
    url,
    headers,
    toString() {
      return url;
    },
  };
}

// Basic response handler with error checking to throws an error for non-200 responses
async function handleResponse(response) {
  // Basic error-checking; throws if the response is not successful
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.text();
}

// Example usage showing two common operations:
// 1. Listing all available buckets
// 2. Listing contents of a specific bucket
(async () => {
  // Configuration for Backblaze B2 specifically
  const region = "eu-central-003";
  let config = {
    region, 
    secretKey: "", // B2 applicationKey
    accessKeyId: "", // B2 keyID
    endpoint: "s3." + region + ".backblazeb2.com",
  };

  // First request: List all buckets available to this account
  const constructedRequest = await constructSignedRequest(config);
  const bucketsResponse = await fetch(constructedRequest.url, {
    headers: constructedRequest.headers,
  });
  console.log("Available buckets:\n", await handleResponse(bucketsResponse));

  // Second request: List files in a specific bucket
  // We scope the request to the bucket:
  config.bucket = "freecords";

  const constructedBucketRequest = await constructSignedRequest(config);
  const filesResponse = await fetch(constructedBucketRequest.url, {
    headers: constructedBucketRequest.headers,
  });
  console.log("Bucket contents:\n", await handleResponse(filesResponse));
})();
