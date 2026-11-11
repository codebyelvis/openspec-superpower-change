// Author: elvis. Governed host-side adapter for agent-autoloop (change integrate-governed-cli-autoloop).
// Passes turn.contextFile so gov_runner.py resolves per-event isolated batch contracts (<batches_dir>/<subject>.json)
// without shared single-file overwrite; stays backward-compatible with static `c.batch` for mechanism fixtures.
import { readFileSync } from "node:fs";
import { join } from "node:path";

const install = () => JSON.parse(readFileSync(join(import.meta.dirname, "install.json"), "utf8"));

export default {
  command(turn) {
    const c = install();
    const batchArgs = c.batches_dir ? ["--batches-dir", c.batches_dir] : ["--batch", c.batch];
    return [
      c.python,
      c.runner,
      ...batchArgs,
      "--context-file",
      turn.contextFile ?? "",
      "--folder",
      turn.folder,
      "--session",
      turn.session,
      "--resume",
      turn.resume ?? "",
      "--cwd",
      turn.cwd,
    ];
  },
  read(stdout, code, stderr) {
    const lines = stdout.split("\n").filter(Boolean);
    const metaLine = lines.findLast((l) => l.startsWith("META:"));
    const meta = metaLine ? JSON.parse(metaLine.slice(5)) : {};
    const text = lines.filter((l) => !l.startsWith("META:")).join("\n");
    const base = { session: meta.session, started: Boolean(meta.started) };
    if (code === null) return { ...base, finished: Boolean(meta.finished) };
    if (code !== 0) return { ...base, error: stderr.trim() || "exit " + code };
    return { ...base, finished: true, text };
  },
  link: (s) => "gov://" + s,
};
