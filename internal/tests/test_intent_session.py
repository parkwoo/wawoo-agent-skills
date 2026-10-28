#!/usr/bin/env python3
"""B3 MCP ゲート・L3 delegate の単体テスト。"""
from __future__ import annotations

import json
import time
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "mcp" / "server.py"
sys.path.insert(0, str(ROOT / "mcp"))

from intent_delegation import build_delegation_payload  # noqa: E402
from intent_steer import build_steer_payload  # noqa: E402
from intent_session import (  # noqa: E402
    activate_schedule,
    check_tool_allowed,
    clear_schedule,
    reset_session,
)

_SESSION = Path(tempfile.mkdtemp(prefix="wawoo-sess-test-")) / "session.json"
os.environ["WAWOO_INTENT_SESSION"] = str(_SESSION)
os.environ["WAWOO_INTENT_RESUME"] = "1"


def rpc(proc, payload: dict) -> dict:
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    return json.loads(line)


def test_session_gate_unit() -> None:
    clear_schedule()
    activate_schedule(
        {
            "workflow": "compliance-review",
            "mcp_tools_allow": [
                "capabilities",
                "skill_search",
                "skill_get",
                "workflow_get",
                "agent_get",
                "memory_recall",
                "evidence_check",
                "interpret_intent",
                "route_task",
            ],
        }
    )
    assert check_tool_allowed("memory_save") is not None
    assert check_tool_allowed("skill_get") is None
    assert check_tool_allowed("workflow_clear") is None
    clear_schedule()
    assert check_tool_allowed("memory_save") is None  # ゲート解除後は全許可


def test_delegation_payload() -> None:
    p = build_delegation_payload(
        {"workflow": "research", "agent": "product-owner", "delegation_hint": "upstream-subagent"},
        subtask="競合3社を調べる",
        label="競合調査",
    )
    assert p["route_layer"] == "L3"
    assert p["parent_workflow"] == "research"
    q = build_delegation_payload({"workflow": "incident-response", "agent": "sre-operator"}, subtask="mitigate", idempotency_key="abc123")
    assert q.get("idempotency_key") == "abc123"
    r = build_delegation_payload({"workflow": "delivery-lite", "agent": "implementer"}, subtask="rename var", model_tier="fast")
    assert r.get("model_tier") == "fast"


def test_mcp_gate_stdio() -> None:
    env = dict(os.environ)
    with tempfile.TemporaryDirectory() as td:
        # テストが実リポジトリの docs/memory を汚さないよう隔離する
        env["WAWOO_MEMORY_ROOT"] = td
        env["WAWOO_INTENT_LEARN_DB"] = str(Path(td) / "learned.db")
        env["WAWOO_INTENT_SESSION"] = str(_SESSION)
        proc = subprocess.Popen(
            [sys.executable, str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(ROOT),
            env=env,
        )
        _run_gate_scenario(proc)


def _run_gate_scenario(proc) -> None:
    try:
        rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}})
        rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "interpret_intent", "arguments": {"text": "/compliance-review ポリシー確認"}}})
        blocked = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "memory_save", "arguments": {"text": "test", "tags": "decision"}},
            },
        )
        assert blocked["result"].get("isError") is True
        assert "outside the allow-set" in blocked["result"]["content"][0]["text"]
        deleg = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "delegate_subtask", "arguments": {"subtask": "条項Aを要約"}},
            },
        )
        assert not deleg["result"].get("isError")
        assert "L3" in deleg["result"]["content"][0]["text"]
        rpc(proc, {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "workflow_clear", "arguments": {}}})
        ok = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {"name": "memory_save", "arguments": {"text": "after clear", "tags": "open"}},
            },
        )
        assert not ok["result"].get("isError")
    finally:
        proc.stdin.close()
        proc.wait(timeout=10)


def test_session_persists_across_restart() -> None:
    reset_session()
    activate_schedule(
        {
            "workflow": "compliance-review",
            "mcp_tools_allow": ["skill_get", "capabilities"],
        }
    )
    assert _SESSION.is_file()
    # Simulate a process restart: drop in-memory state but keep the file.
    reset_session(delete=False)
    assert check_tool_allowed("memory_save") is not None  # gate restored from disk
    assert check_tool_allowed("skill_get") is None
    reset_session()



def test_steer_payload() -> None:
    need = build_steer_payload(text="add a regression test", root=ROOT, active_workflow="delivery-lite")
    assert need["kind"] == "amend" and need["needs_classification"] is True
    assert "plan" in need
    done = build_steer_payload(text="add a regression test", root=ROOT, active_workflow="delivery-lite", op="add")
    assert done["needs_classification"] is False and done["op"] == "add" and done["applied"] is False


def test_session_not_persisted_when_resume_off() -> None:
    os.environ.pop("WAWOO_INTENT_RESUME", None)
    reset_session()
    try:
        activate_schedule({"workflow": "delivery-lite", "mcp_tools_allow": ["skill_get"]})
        assert not _SESSION.is_file()
    finally:
        os.environ["WAWOO_INTENT_RESUME"] = "1"
        reset_session()


def test_session_ttl_expiry() -> None:
    os.environ["WAWOO_INTENT_RESUME"] = "1"
    reset_session()
    activate_schedule({"workflow": "delivery-lite", "mcp_tools_allow": ["skill_get"]})
    data = json.loads(_SESSION.read_text(encoding="utf-8"))
    data["_saved_at"] = time.time() - 13 * 3600
    _SESSION.write_text(json.dumps(data), encoding="utf-8")
    reset_session(delete=False)
    assert check_tool_allowed("memory_save") is None  # stale gate not restored
    assert not _SESSION.exists()  # stale file removed
    reset_session()


def test_session_client_scoped_path() -> None:
    import intent_session as S

    saved = os.environ.pop("WAWOO_INTENT_SESSION", None)
    saved_root = os.environ.get("WAWOO_SKILLS_ROOT")
    tmp = Path(tempfile.mkdtemp(prefix="wawoo-client-"))
    os.environ["WAWOO_SKILLS_ROOT"] = str(tmp)
    os.environ["WAWOO_INTENT_CLIENT"] = "kilo"
    try:
        p = S._session_path()
        assert p.name == "intent_session.kilo.json"
        assert p.parent == tmp / "data"
    finally:
        os.environ.pop("WAWOO_INTENT_CLIENT", None)
        if saved is not None:
            os.environ["WAWOO_INTENT_SESSION"] = saved
        if saved_root is None:
            os.environ.pop("WAWOO_SKILLS_ROOT", None)
        else:
            os.environ["WAWOO_SKILLS_ROOT"] = saved_root

def main() -> int:
    test_session_gate_unit()
    test_delegation_payload()
    test_mcp_gate_stdio()
    test_session_persists_across_restart()
    test_steer_payload()
    test_session_not_persisted_when_resume_off()
    test_session_ttl_expiry()
    test_session_client_scoped_path()
    print("intent_session tests: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
