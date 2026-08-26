#!/usr/bin/env node
// Evaluate ExtendScript (JSX) inside Premiere via the MCP Bridge CEP panel's CDP port.
// Usage: node pr_jsx_eval.mjs 'app.project.name'
import { readFileSync } from 'node:fs';

const expr = process.argv[2];
const jsx = expr.startsWith('@') ? readFileSync(expr.slice(1), 'utf8') : expr;

const port = process.env.PR_CDP_PORT || 8877;
const targets = await (await fetch(`http://localhost:${port}/json`)).json();
const page = targets.find(t => t.title.includes('MCP Bridge'));
if (!page) { console.error('MCP Bridge panel not found'); process.exit(1); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0;
const send = (method, params) => ws.send(JSON.stringify({ id: ++id, method, params }));
const evalJs = (expression) => new Promise((resolve) => {
  const myId = ++id;
  const onMsg = (e) => {
    const d = JSON.parse(e.data);
    if (d.id === myId) { ws.removeEventListener('message', onMsg); resolve(d.result?.result?.value); }
  };
  ws.addEventListener('message', onMsg);
  ws.send(JSON.stringify({ id: myId, method: 'Runtime.evaluate', params: { expression, returnByValue: true, awaitPromise: true } }));
});

ws.onopen = async () => {
  await evalJs(`window.__jsxDone=false; window.__jsxResult=undefined;
    new CSInterface().evalScript(${JSON.stringify(jsx)}, function(x){ window.__jsxResult=x; window.__jsxDone=true; }); "sent"`);
  for (let i = 0; i < 40; i++) {
    await new Promise(r => setTimeout(r, 250));
    if (await evalJs('window.__jsxDone')) {
      console.log(await evalJs('window.__jsxResult'));
      ws.close(); process.exit(0);
    }
  }
  console.error('JSX eval timeout'); process.exit(1);
};
setTimeout(() => { console.error('CDP timeout'); process.exit(1); }, 15000);
