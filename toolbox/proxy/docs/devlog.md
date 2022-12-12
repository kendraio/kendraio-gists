https://blog.logrocket.com/how-to-set-up-node-typescript-express/

curl https://echo.hyperdata.it --proxy 127.0.0.1:3003

curl https://echo.hyperdata.it --proxy localhost:3003

npm install -g ts-node

ts-node index.ts

broken install...

// sudo npm install -g @angular/cli

kendraio-app

git clone

npm install

got some version? error with angular, added --force

rm -r /home/danny/kendraio/kendraio-app/node_modules

npm cache clean --force

npm install --force

npm cache clean -f

npm run start:dev

    "lodash": "^4.17.21",
    "lodash-es": "^4.17.21",

./node_modules/lodash-es/object.js:35:0-44 - Error: export '[object Set]' (reexported as 'pick') was not found in './pick.js' (possible exports: default)

ng serve --verbose

ran!!!

tried swapping, around line 97 of http-block-component.ts

const defaultProxy = get(appSettings, 'defaultCorsProxy', 'https://proxy.kendra.io/');

const defaultProxy = get(appSettings, 'defaultCorsProxy', 'http://localhost:3003/');

the view source was fine but wasn't rendered - not getting .js files?

---

hmm, kendraio-proxy/vercel.json

has
{
"rewrites": [
{ "source": "/", "destination": "/api/proxy" },
{ "source": "/:path", "destination": "/api/proxy" }
]
}

api/proxy.js

Error: This command is not available when running the Angular CLI outside a workspace.

- needs a angular.json ?

running proxy.js exits immediately

needs an angular runner?
