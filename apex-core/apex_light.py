import os
from dotenv import load_dotenv

class ApexLight:
    def __init__(self, mem0_key=None):
        load_dotenv()
        self.mem0_key = mem0_key or os.getenv("MEM0_API_KEY")
        self.mcp_id = os.getenv("MCP_GLOBAL_ID")
        
    def execute(self, task):
        print(f"🚀 Apex Oracle [GUID: {self.mcp_id}] processing task: {task}")
        # Logic to interface with MemoryPlugin/MCP tools would go here
        return f"Task '{task}' initiated with Mem0 key {self.mem0_key[:5]}..."

if __name__ == "__main__":
    agent = ApexLight()
    print(agent.execute("Sync Notion database with GitHub repo"))
