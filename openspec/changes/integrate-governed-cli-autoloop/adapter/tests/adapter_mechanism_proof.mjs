// Author: elvis. Mechanism proof of the governed host-side adapter against the unmodified ~/.agent-autoloop/app engine.
// `attempts` in the hub counts failed attempts; the ledger records the dispatch attempt number.
// Usage: node adapter_mechanism_proof.mjs <persistent-proof-dir>
import { mkdirSync, readFileSync, writeFileSync, existsSync, copyFileSync, readdirSync, renameSync } from "node:fs";
import { join, dirname } from "node:path";
import { pathToFileURL } from "node:url";

const SRC = dirname(dirname(new URL(import.meta.url).pathname));
const P = process.argv[2];
const HOME = join(P, "autoloop-home");
const PLUG = join(HOME, "plugins", "govpi");
mkdirSync(PLUG, { recursive: true });
mkdirSync(join(P, "fixture-cwd"), { recursive: true });
copyFileSync(join(SRC, "govpi", "agent.ts"), join(PLUG, "agent.ts"));
const BATCH = join(P, "batch.json");
writeFileSync(join(PLUG, "install.json"), JSON.stringify({ python: "/usr/bin/python3", runner: join(SRC, "gov_runner.py"), batch: BATCH }));
process.env.GOV_PROOF_DIR = P;
writeFileSync(join(P, "cli-launches.log"), "");
const setBatch = (batch_id, expected_resume, stub_mode) => writeFileSync(BATCH, JSON.stringify({
  batch_id, expected_resume, stub_mode, mode: "stub", allow_rerun: false,
  cli_cmd: ["/bin/sh", join(SRC, "tests", "fake_cli.sh")],
  stop_cmd: ["/usr/bin/python3", join(SRC, "tests", "stop_stub.py")],
  ledger_dir: join(P, "ledger"), evidence_dir: join(P, "evidence"),
}, null, 2));

writeFileSync(join(P, "rules.fixture.json"), JSON.stringify({
  timezone: "Asia/Shanghai", sources: { gov: { name: "治理门禁" } },
  agents: { "gov-agent": { name: "受控适配器", worker: "w1", use: "govpi", access: "read", timeout: 1 } },
  channels: { chat: { name: "聊天", answerers: ["me"] } },
  rules: [{ name: "适配器探针", when: { source: "gov", types: ["verify.*"] }, to: "gov-agent", cwd: join(P, "fixture-cwd"),
    prompt: "执行VERIFY探针。", group: "gov", parallel: 2, resume: true }],
  elsewhere: [],
}, null, 2));
process.env.AGENT_AUTOLOOP_HOME = HOME;
process.env.AGENT_AUTOLOOP_RULES = join(P, "rules.fixture.json");
process.env.AGENT_AUTOLOOP_PUBLIC_URL = "https://hub.test";

const appRoot = "/Users/elvis/.agent-autoloop/app";
const hub = await import(pathToFileURL(join(appRoot, "tests/hub.ts")).href);
const { createWorker } = await import(pathToFileURL(join(appRoot, "worker/worker.ts")).href);

let clock = Date.parse("2026-11-09T12:00:00.000Z");
const logs = [];
const stops = [];
const worker = createWorker({
  hub: {
    async work({ claim }) { hub.heartbeat("w1", [], clock); const cancel = hub.cancels("w1"); const job = hub.claimNext("w1", claim, clock); return { cancel, ...(job ? { job } : {}) }; },
    async started(run, token, info) { hub.started(run, token, info, clock); },
    async result(run, token, result) { return hub.finish(run, token, result, clock); },
  },
  name: "w1", log: (l) => logs.push(l), now: () => clock,
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function serviceStops() {
  const d = join(P, "stop-requests");
  if (!existsSync(d)) return;
  for (const f of readdirSync(d).filter((x) => x.endsWith(".req"))) {
    const run = Number(readFileSync(join(d, f), "utf8"));
    let out;
    try { hub.cancel(run, clock); out = "cancel accepted"; } catch (e) { out = "cancel error: " + e.message; }
    stops.push({ run, out, state_after: hub.getView().get("runs", run).state, cancel_at: hub.getView().get("runs", run).cancel_at });
    writeFileSync(join(d, f.replace(/\.req$/, ".ack")), out);
    renameSync(join(d, f), join(d, f + ".done"));
  }
}
async function settle(maxMs = 5000) {
  const start = Date.now();
  while (Date.now() - start < maxMs) {
    serviceStops();
    const held = worker.entries();
    if (!held.length || held.every((e) => existsSync(join(e.dir, `exit-${e.turn}`)))) return;
    await sleep(50);
  }
}
async function cycle(n = 1) { for (let i = 0; i < n; i++) { await worker.tick(); await settle(); } }
const cli = (run) => readFileSync(join(P, "cli-launches.log"), "utf8").split("\n").filter((l) => l.startsWith(run + "|"));
const view = (id) => { const r = hub.getView().get("runs", id); return { id, state: r.state, attempts: r.attempts, resume: r.resume, session: r.session, summary: r.summary, error: r.error, not_before: r.not_before }; };
const ledger = (b) => existsSync(join(P, "ledger", b + ".json")) ? JSON.parse(readFileSync(join(P, "ledger", b + ".json"), "utf8")).launches : [];
const abort = (run) => existsSync(join(P, "evidence", `run-${run}`, "report-abort.md"));
async function drainRetry(id, rounds = 4) {
  for (let i = 0; i < rounds; i++) {
    const r = hub.getView().get("runs", id);
    if (["done", "cancelled", "nothing"].includes(r.state)) return;
    if (r.not_before) clock = Date.parse(r.not_before) + 1000;
    await cycle(2);
  }
}
const R = {};

setBatch("seed-a", null, "seed");
hub.ingest("gov", { id: "ev-seed-a", type: "verify.seed", subject: "lane-a" }, clock);
await cycle(2);
R.seed_a = view(1);

setBatch("s1-verify-fail", "bound-session-001", "report_fail"); clock += 1000;
hub.ingest("gov", { id: "ev-s1", type: "verify.run", subject: "lane-a" }, clock);
await cycle(2);
R.s1_business_verify_fail = { run: view(2), cli_launches: cli(2), report: readFileSync(join(P, "evidence/run-2/report.md"), "utf8").trim(), ledger: ledger("s1-verify-fail") };

setBatch("s2-cli-fault", "bound-session-001", "fault"); clock += 1000;
hub.ingest("gov", { id: "ev-s2", type: "verify.run", subject: "lane-a" }, clock);
await cycle(3);
R.s2_cli_fault_triedFresh = { run: view(3), cli_launches: cli(3), ledger: ledger("s2-cli-fault"), report_abort: abort(3), worker_log: logs.filter((l) => l.includes("run 3")) };

setBatch("s3-caller-killed", null, "kill_parent"); clock += 1000;
hub.ingest("gov", { id: "ev-s3", type: "verify.run", subject: "lane-k" }, clock);
await cycle(2);
R.s3_after_attempt1 = view(4);
await drainRetry(4);
R.s3_caller_killed_retryLater = { run: view(4), cli_launches: cli(4), ledger: ledger("s3-caller-killed"), report_abort: abort(4), worker_log: logs.filter((l) => l.includes("run 4")) };

setBatch("s4-worker-timeout", null, "hang"); clock += 1000;
hub.ingest("gov", { id: "ev-s4", type: "verify.run", subject: "lane-t" }, clock);
await worker.tick(); await sleep(400); await worker.tick();
clock += 61_000; await worker.tick(); await sleep(400); await worker.tick(); await settle();
R.s4_after_timeout = view(5);
await drainRetry(5);
R.s4_worker_timeout_retryLater = { run: view(5), cli_launches: cli(5), ledger: ledger("s4-worker-timeout"), report_abort: abort(5), worker_log: logs.filter((l) => l.includes("run 5")) };

setBatch("seed-u", null, "seed"); clock += 1000;
hub.ingest("gov", { id: "ev-seed-u", type: "verify.seed", subject: "lane-u" }, clock);
await cycle(2);
R.seed_u = view(6);
clock += 1000;
hub.ingest("gov", { id: "ev-u-stuck", type: "verify.run", subject: "lane-u" }, clock);
const job7 = hub.claimNext("w1", "claim-run-7", clock);
clock += 6 * 60_000; hub.heartbeat("w1", [], clock); hub.sweep(clock);
R.run7_unknown = { claimed_session: job7.session, ...view(7) };
setBatch("s5-unknown-settle", "bound-session-001", "seed"); clock += 1000;
hub.ingest("gov", { id: "ev-u-follow", type: "verify.run", subject: "lane-u" }, clock);
await cycle(3);
R.s5_unknown_settleSession = { run: view(8), cli_launches: cli(8), ledger: ledger("s5-unknown-settle"), report_abort: abort(8) };

setBatch("seed-m", null, "seed"); clock += 1000;
hub.ingest("gov", { id: "ev-seed-m", type: "verify.seed", subject: "lane-m" }, clock);
await cycle(2);
R.seed_m = view(9);
setBatch("s6-post-output-mismatch", "bound-session-001", "wrong_session"); clock += 1000;
hub.ingest("gov", { id: "ev-s6", type: "verify.run", subject: "lane-m" }, clock);
await cycle(2);
R.s6_post_output_mismatch = { run: view(10), cli_launches: cli(10), ledger: ledger("s6-post-output-mismatch"), report_abort: abort(10) };

R.stop_requests_serviced = stops;

const ok = (c, m) => (c ? null : m);
R.assertions = [
  ok(R.s1_business_verify_fail.run.state === "done" && R.s1_business_verify_fail.cli_launches.length === 1 && R.s1_business_verify_fail.report.startsWith("VERIFY: FAIL"), "s1"),
  ok(R.s2_cli_fault_triedFresh.cli_launches.length === 1 && R.s2_cli_fault_triedFresh.run.attempts === 0 && R.s2_cli_fault_triedFresh.run.state === "done" && R.s2_cli_fault_triedFresh.report_abort && R.s2_cli_fault_triedFresh.ledger[1]?.resume_arg === null, "s2"),
  ok(R.s3_caller_killed_retryLater.cli_launches.length === 1 && R.s3_caller_killed_retryLater.run.attempts === 1 && R.s3_caller_killed_retryLater.ledger[1]?.attempt === 2 && R.s3_caller_killed_retryLater.run.summary.startsWith("执行中止：重派被拦截") && ["cancelled", "done"].includes(R.s3_caller_killed_retryLater.run.state) && R.s3_caller_killed_retryLater.ledger[1]?.action === "stop", "s3"),
  ok(R.s4_worker_timeout_retryLater.cli_launches.length === 1 && R.s4_worker_timeout_retryLater.run.attempts === 1 && R.s4_worker_timeout_retryLater.ledger[1]?.attempt === 2 && R.s4_worker_timeout_retryLater.run.summary.startsWith("执行中止：重派被拦截") && ["cancelled", "done"].includes(R.s4_worker_timeout_retryLater.run.state) && R.s4_worker_timeout_retryLater.ledger[1]?.action === "stop", "s4"),
  ok(R.s5_unknown_settleSession.cli_launches.length === 0 && R.s5_unknown_settleSession.run.state === "done" && R.s5_unknown_settleSession.report_abort, "s5"),
  ok(R.s6_post_output_mismatch.cli_launches.length === 1 && R.s6_post_output_mismatch.run.state === "done" && R.s6_post_output_mismatch.run.attempts === 0 && R.s6_post_output_mismatch.report_abort && R.s6_post_output_mismatch.run.summary.startsWith("执行中止：结果后会话身份不符"), "s6"),
].filter(Boolean);
writeFileSync(join(P, "adapter-mechanism-results.json"), JSON.stringify(R, null, 2) + "\n");
console.log(JSON.stringify(R, null, 2));
process.exit(R.assertions.length ? 1 : 0);
