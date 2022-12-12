const http = require('http')
const server = http.createServer()

server
  .on('request', (request, response) => {
    let body = []

    request
      .on('data', chunk => {
        body.push(chunk)
      })
      .on('end', () => {
        body = Buffer.concat(body).toString()
        response.statusCode = 200

        /* CORS */
        response.setHeader('Access-Control-Allow-Origin', '*')
        response.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET')
        response.setHeader('Access-Control-Allow-Headers', 'Accept')
        response.setHeader('Access-Control-Max-Age', 2592000) // 30 days -  preflight request cache time

        // hacky
        if (request.headers.accept.startsWith('application/json')) {
          response.setHeader('Content-Type', 'application/json')
          response.write(JSON.stringify(request.headers))
        } else {
          // default to HTML
          response.setHeader('Content-Type', 'text/html')
          response.write(`${request.method} ${request.url}`) // for now
          response.write(toHTML(JSON.parse(JSON.stringify(request.headers)))) // crazy but true
        }
        response.end()
      })
  })
  .listen(3001)

function toHTML (json) {
  var html = '<html><body>'

  for (var key in json) {
    html += '<strong>' + key + '</strong> : ' + json[key] + '<br/>'
  }

  html += '</body></html>'
  return html
}
