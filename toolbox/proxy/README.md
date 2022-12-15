# typescript-proxy

## Simple HTTP Proxy

Written in typescript for node.js, using Express, see https://blog.logrocket.com/how-to-set-up-node-typescript-express/

Supports https

Hardcoded (towards end of script) to run on port 3003

### Compile

from proxy/ dir :

npm install

tsc

or

tsc -w -p .

(watch mode)

### Run

node dist/index.js

or

sudo npm install -g ts-node

then

ts-node index.ts

or

npx ts-node index.ts

#### Run as Service

sudo apt install pm2

pm2 start dist/index.js -n toolbox-proxy

### Test

[to check]

curl https://www.kendra.io/ --proxy http://localhost:3003
