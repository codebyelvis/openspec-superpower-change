#!/bin/sh
# Author: elvis. Disposable stub CLI for the adapter mechanism proof.
mode="$1"; resume="$2"
echo "${AGENT_AUTOLOOP_RUN}|${mode}|${resume}|$$" >> "${GOV_PROOF_DIR:-$(dirname "$0")}/cli-launches.log"
case "$mode" in
  seed) echo STARTED; echo SESSION:bound-session-001; echo "报告已交付：R1 会话已建立"; exit 0 ;;
  report_fail) echo STARTED; echo SESSION:${resume}; echo "VERIFY: FAIL（业务失败，不重跑不转FIX）"; exit 0 ;;
  fault) echo "CLI startup error before started" >&2; exit 1 ;;
  kill_parent) echo STARTED; echo SESSION:sess-k; sleep 0.3; kill -9 $PPID; sleep 1; exit 0 ;;
  hang) echo STARTED; echo SESSION:sess-t; sleep 30 ;;
  wrong_session) echo STARTED; echo SESSION:wrong-session-999; echo "done"; exit 0 ;;
  *) echo "unknown mode $mode" >&2; exit 9 ;;
esac
