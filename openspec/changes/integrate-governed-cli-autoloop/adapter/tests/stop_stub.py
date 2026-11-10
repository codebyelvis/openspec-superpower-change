#!/usr/bin/env python3
# Author: elvis. Harness-only stand-in for `agent-autoloop stop <run>`: the in-process hub services the request
# with the same kernel `cancel` action that ownerClient().cancel reaches over HTTP.
import os, sys, time
from pathlib import Path
d = Path(os.environ.get("GOV_PROOF_DIR", Path(__file__).parent)) / "stop-requests"
d.mkdir(parents=True, exist_ok=True)
req = d / f"{sys.argv[1]}-{time.time_ns()}.req"
req.write_text(sys.argv[1])
for _ in range(200):
    if req.with_suffix(".ack").exists():
        print(req.with_suffix(".ack").read_text()); sys.exit(0)
    time.sleep(0.05)
sys.exit(5)
