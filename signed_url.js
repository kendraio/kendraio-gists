async function s3LikeSignedUrl(appKey, keyID, baseUrl, path, expiry) {
  const exp = Math.floor(Date.now() / 1000) + expiry;
  const toSign = `${path}\n${exp}`;
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(appKey), { name: 'HMAC', hash: 'SHA-1' }, false, ['sign']
  );
  const sigBuffer = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(toSign));
  const sig = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
  return `${baseUrl}/${encodeURIComponent(path)}?Authorization=${keyID}:${sig}&Expires=${exp}`;
}

// Example use:
(async () => {
  console.log(await s3LikeSignedUrl('insert-app-key-here', 'insert-key-id-here', 'https://s3.eu-central-003.backblazeb2.com', 'path/to/file', 3600));
})();