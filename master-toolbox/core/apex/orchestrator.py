import asyncio
import json
import os
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Protocol

# --- Existing imports ---
from core.apex.engine import ApexMem0Master
from core.apex.multi_memory import MultiMemoryOrchestrator
from core.apex.mcp_client import McpCliClient
from core.apex.notion_router import NotionMcpRouter

# =========================
# Adapters (Pluggable)
# =========================

class EventBus(Protocol):
    async def publish(self, topic: str, message: Dict[str, Any]) -> None: ...
    async def request(self, topic: str, message: Dict[str, Any], timeout_s: float = 30) -> Dict[str, Any]: ...

class MCPClient(Protocol):
    async def call(self, server: str, tool: str, params: Dict[str, Any]) -> Dict[str, Any]: ...

class SandboxRunner(Protocol):
    async def run(self, code: str, meta: Dict[str, Any]) -> Dict[str, Any]: ...

class ApiGateway(Protocol):
    async def post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]: ...

# =========================
# Minimal built-in impls
# =========================

class InMemoryBus:
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}

    def _q(self, topic: str) -> asyncio.Queue:
        if topic not in self._queues:
            self._queues[topic] = asyncio.Queue()
        return self._queues[topic]

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        await self._q(topic).put(message)

    async def request(self, topic: str, message: Dict[str, Any], timeout_s: float = 30) -> Dict[str, Any]:
        reply_topic = message.get("reply_topic") or f"reply:{uuid.uuid4()}"
        message["reply_topic"] = reply_topic
        await self.publish(topic, message)
        try:
            reply = await asyncio.wait_for(self._q(reply_topic).get(), timeout=timeout_s)
            return reply
        except asyncio.TimeoutError:
            return {"ok": False, "error": f"timeout waiting for {reply_topic}", "topic": topic}

class NullSandboxRunner:
    async def run(self, code: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "result": "Sandbox runner placeholder", "code_preview": code[:120], "meta": meta}

class NullApiGateway:
    async def post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "error": "API gateway not configured", "endpoint": endpoint, "payload_keys": list(payload.keys())}

# =========================
# Audit (append-only JSONL)
# =========================

class JsonlAudit:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def write(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event["ts"] = event.get("ts") or time.time()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")

@dataclass
class OrchestratorResult:
    ok: bool
    run_id: str
    steps: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# =========================
# Apex Orchestrator v3.6 Ω
# =========================

class ApexOrchestrator:
    def __init__(
        self,
        bus: Optional[EventBus] = None,
        mcp: Optional[MCPClient] = None,
        sandbox: Optional[SandboxRunner] = None,
        api: Optional[ApiGateway] = None,
        audit_path: str = "/home/user/master-toolbox/logs/apex_audit.jsonl",
    ):
        self.engine = ApexMem0Master()
        self.memory = MultiMemoryOrchestrator()
        self.bus = bus or InMemoryBus()
        self.mcp = mcp or McpCliClient(timeout_s=60)
        self.notion = NotionMcpRouter(self.mcp, servers=["notion", "smithery-notion", "mingxiao300-notion-smithery"])
        self.sandbox = sandbox or NullSandboxRunner()
        self.api = api or NullApiGateway()
        self.audit = JsonlAudit(audit_path)
        print("🌌 Apex Universal Orchestrator: INITIALIZED (v3.6 Ω)")

    async def a2a_handshake(self, source_agent: str, target_agent: str, task: str, case_id: Optional[str] = None):
        msg = {
            "op": "a2a.delegate",
            "from": source_agent,
            "to": target_agent,
            "task": task,
            "case_id": case_id,
            "run_id": str(uuid.uuid4()),
        }
        self.audit.write({"stage": "A2A", "event": msg})
        await self.bus.publish(f"agent:{target_agent}", msg)
        return {"ok": True, "status": "delegated", **msg}

    async def a2s_synthesis(self, agent_data: List[Dict[str, Any]], case_id: Optional[str] = None):
        payload = {"op": "a2s.synthesize", "case_id": case_id, "agent_data": agent_data}
        self.audit.write({"stage": "A2S", "event": {"case_id": case_id, "agents": [a.get("agent") for a in agent_data]}})
        results = {}
        try:
            results["mem0_master"] = await self.engine.ingest(payload)
        except Exception as e:
            results["mem0_master"] = {"ok": False, "error": str(e)}
        try:
            results["multi_memory"] = await self.memory.sink(payload)
        except Exception as e:
            results["multi_memory"] = {"ok": False, "error": str(e)}
        self.audit.write({"stage": "A2S", "result": results})
        return {"ok": True, "status": "synthesized", "results": results}

    async def e2b_execution(self, code: str, case_id: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
        meta = meta or {}
        meta["case_id"] = case_id
        self.audit.write({"stage": "E2B", "code_preview": code[:200], "meta": meta})
        res = await self.sandbox.run(code, meta=meta)
        self.audit.write({"stage": "E2B", "result": res})
        return res

    async def mcp_bridge(self, server: str, tool: str, params: Dict[str, Any], case_id: Optional[str] = None):
        self.audit.write({"stage": "MCP", "server": server, "tool": tool, "case_id": case_id, "params_keys": list(params.keys())})
        res = await self.mcp.call(server, tool, params)
        self.audit.write({"stage": "MCP", "result": res})
        return res

    async def notion_health(self):
        res = await self.notion.health_check()
        self.audit.write({"stage": "NOTION", "event": "health_check", "result": res})
        return res

    async def powerhouse_workflow(self, case_update: str, case_id: str = "1FDV-23-0001009") -> OrchestratorResult:
        run_id = str(uuid.uuid4())
        steps: List[Dict[str, Any]] = []
        errors: List[Dict[str, Any]] = []
        self.audit.write({"stage": "RUN", "run_id": run_id, "case_id": case_id, "event": "powerhouse.start"})
        try:
            s1 = await self.a2s_synthesis([{"agent": "Operator", "note": case_update}], case_id=case_id)
            steps.append({"step": "A2S", "result": s1})
        except Exception as e:
            errors.append({"step": "A2S", "error": str(e)})
        try:
            # Using real Supabase check via MCP Client
            s2 = await self.mcp_bridge("supabase-f597", "execute_sql", {"sql": "SELECT 1"}, case_id=case_id)
            steps.append({"step": "SUPABASE", "result": s2})
        except Exception as e:
            errors.append({"step": "SUPABASE", "error": str(e)})
        try:
            s3 = await self.e2b_execution("verify_file_integrity()", case_id=case_id, meta={"run_id": run_id})
            steps.append({"step": "E2B", "result": s3})
        except Exception as e:
            errors.append({"step": "E2B", "error": str(e)})
        try:
            # Fixed Notion call params
            s4 = await self.notion.call("append-block-children", {
                "blockId": "172b1e4f322380b8bc63dc0726949795", 
                "children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"[{time.ctime()}] APEX Update: {case_update}"}}]}}]
            })
            steps.append({"step": "NOTION", "result": s4})
        except Exception as e:
            errors.append({"step": "NOTION", "error": str(e)})
        ok = len(errors) == 0
        self.audit.write({"stage": "RUN", "run_id": run_id, "case_id": case_id, "event": "powerhouse.end", "ok": ok, "errors": errors})
        return OrchestratorResult(ok=ok, run_id=run_id, steps=steps, errors=errors)

orchestrator = ApexOrchestrator()
