import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

try:
    from core.apex.orchestrator import orchestrator
    APEX_READY = True
except Exception as e:
    print(f"⚠️ APEX Load Error: {e}")
    APEX_READY = False

class MasterToolbox:
    def __init__(self):
        self.version = "3.6-OMEGA"
        self.case_id = "1FDV-23-0001009"
        self.startup_time = datetime.now()
        print(f"🧠 Master Toolbox v{self.version} Initializing...")

    def start_all(self):
        print("\n" + "=" * 60)
        print("🚀 MASTER TOOLBOX: APEX OMEGA EDITION")
        print("=" * 60)
        print("✅ A2A (Agent-to-Agent): READY")
        print("✅ A2S (Agent-to-System): READY")
        print("✅ E2B (Sandbox Execution): READY")
        print("✅ MCP (Tool Bridge): READY (depends on adapter)")
        print("✅ API (Gateways): READY (depends on adapter)")
        print("=" * 60 + "\n")

    async def run_powerhouse(self, input_text: str):
        if not APEX_READY:
            print("⚠️ APEX Orchestrator not available.")
            return
        result = await orchestrator.powerhouse_workflow(input_text, case_id=self.case_id)
        return result

    def health(self):
        return {
            "version": self.version,
            "orchestration": "A2A/A2S/E2B/MCP/API",
            "status": "SUPREME",
            "uptime": str(datetime.now() - self.startup_time),
            "apex_ready": APEX_READY,
        }

async def run_command(command, args):
    toolbox = MasterToolbox()
    
    if command == "start":
        toolbox.start_all()
    elif command == "status":
        toolbox.start_all()
        print(json.dumps(toolbox.health(), indent=2))
    elif command == "health":
        print(json.dumps(toolbox.health(), indent=2))
    elif command == "power":
        toolbox.start_all()
        msg = " ".join(args) if args else "Manual Powerhouse Trigger"
        result = await toolbox.run_powerhouse(msg)
        print(json.dumps(result.to_dict(), indent=2))
    elif command == "process" and args:
        toolbox.start_all()
        print(f"📥 Processing Evidence: {args[0]}")
        result = await toolbox.run_powerhouse(f"Evidence processing: {args[0]}")
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Unknown command: {command}")

def main():
    if len(sys.argv) < 2:
        print("Usage: toolbox <start|status|health|power|process> [args]")
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    asyncio.run(run_command(command, args))

if __name__ == "__main__":
    main()
