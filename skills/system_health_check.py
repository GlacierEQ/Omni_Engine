import subprocess
import json
import concurrent.futures

CORE_SERVERS = [
    "linear", "github", "notion", "supabase-f597", "google-docs", "exa", 
    "perplexity-mcp", "filesystem", "browser-tool", "sequential-thinking"
]

def check_server(slug):
    try:
        # Check if server exists and list tools (first page)
        result = subprocess.run(["mcp", "--json", slug], capture_output=True, text=True)
        if result.returncode != 0:
            return slug, "MISSING", None
        
        data = json.loads(result.stdout)
        tools = data.get("tools", [])
        
        # Try a simple auth check for some
        status = "INSTALLED"
        if slug == "linear":
            auth_check = subprocess.run(["mcp", slug, "list_issues", "{\"filter\": {}}"], capture_output=True, text=True)
            if "Unauthorized" in auth_check.stdout or "Unauthorized" in auth_check.stderr:
                status = "UNAUTHORIZED"
        elif slug == "github":
            auth_check = subprocess.run(["mcp", slug, "get_the_authenticated_user", "{}"], capture_output=True, text=True)
            if "error" in auth_check.stdout.lower() or "error" in auth_check.stderr.lower():
                status = "AUTH_ERROR"
        
        return slug, status, len(tools)
    except Exception as e:
        return slug, f"ERROR: {str(e)}", None

def run_health_check():
    print("🔍 AUDITING MCP POWERHOUSE...")
    print("-" * 50)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_server, CORE_SERVERS))
    
    for slug, status, tool_count in results:
        tool_str = f"({tool_count} tools)" if tool_count is not None else ""
        print(f"[{status:^12}] {slug:<20} {tool_str}")

if __name__ == "__main__":
    run_health_check()
