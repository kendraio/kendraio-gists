// Import of net module
const net = require("net");
const server = net.createServer();

// yeek! that was the auto-suggestion
server.on("connection", (clientToProxySocket: { once: (arg0: string, arg1: (data: any) => void) => void; write: (arg0: string) => void; pipe: (arg0: any) => void; on: (arg0: string, arg1: (err: any) => void) => void; }) => {
  console.log("Client connected to proxy");
  clientToProxySocket.once("data", (data) => {
    let isTLSConnection = data.toString().indexOf("CONNECT") !== -1;

    let serverPort = 80;
    let serverAddress;
    console.log(data.toString());
    if (isTLSConnection) {
      serverPort = 443;
      serverAddress = data
        .toString()
        .split("CONNECT")[1]
        .split(" ")[1]
        .split(":")[0];
    } else {
      serverAddress = data.toString().split("Host: ")[1].split("\r\n")[0];
    }
    console.log(serverAddress);

    // Creating a connection from proxy to destination server
    let proxyToServerSocket = net.createConnection(
      {
        host: serverAddress,
        port: serverPort,
      },
      () => {
        console.log("Proxy to server set up");
      }
    );


    if (isTLSConnection) {
      clientToProxySocket.write("HTTP/1.1 200 OK\r\n\r\n");
    } else {
      proxyToServerSocket.write(data);
    }

    clientToProxySocket.pipe(proxyToServerSocket);
    proxyToServerSocket.pipe(clientToProxySocket);

    proxyToServerSocket.on("error", (err: any) => {
      console.log("Proxy to server error");
      console.log(err);
    });

    clientToProxySocket.on("error", (err) => {
      console.log("Client to proxy error");
      console.log(err)
    });
  });
});

server.on("error", (err: any) => {
  console.log("Some internal server error occurred");
  console.log(err);
});

server.on("close", () => {
  console.log("Client disconnected");
});

/*
server.on("end", () => {
  console.log("End.");
});
*/

server.listen(
  {
    host: "0.0.0.0",
    port: 3003,
  },
  () => {
    console.log("Server listening on 0.0.0.0:3002");
  }
);
