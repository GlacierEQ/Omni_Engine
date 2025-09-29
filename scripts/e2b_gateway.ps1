# E2B Gateway PowerShell Script for Omni Engine MCP Integration
# Provides secure execution gateway for AI-powered legal intelligence operations

param(
    [Parameter(Mandatory=$true)]
    [string]$Cmd,
    
    [string]$WorkingDirectory = (Get-Location).Path,
    
    [string]$LogFile = "omni_engine_e2b.log",
    
    [switch]$Verbose,
    
    [switch]$DryRun,
    
    [string]$Environment = "development",
    
    [string]$MCPConfig = "mcp_config.json"
)

# Initialize logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    if ($Verbose) {
        Write-Host $logEntry -ForegroundColor $(if($Level -eq "ERROR"){"Red"} elseif($Level -eq "WARN"){"Yellow"} else {"Green"})
    }
    
    Add-Content -Path $LogFile -Value $logEntry -ErrorAction SilentlyContinue
}

# Security validation
function Test-CommandSecurity {
    param([string]$Command)
    
    $dangerousCommands = @(
        'rm -rf /', 'del /s /q', 'format', 'diskpart', 'reg delete',
        'net user', 'net localgroup', 'shutdown', 'restart-computer'
    )
    
    foreach ($dangerous in $dangerousCommands) {
        if ($Command -match [regex]::Escape($dangerous)) {
            return $false
        }
    }
    
    return $true
}

# Load MCP configuration
function Get-MCPConfig {
    param([string]$ConfigPath)
    
    if (-not (Test-Path $ConfigPath)) {
        Write-Log "MCP config not found: $ConfigPath" "WARN"
        return @{}
    }
    
    try {
        $config = Get-Content $ConfigPath | ConvertFrom-Json
        Write-Log "MCP configuration loaded successfully" "INFO"
        return $config
    } catch {
        Write-Log "Failed to parse MCP config: $($_.Exception.Message)" "ERROR"
        return @{}
    }
}

# Initialize environment
function Initialize-Environment {
    param([hashtable]$Config)
    
    Write-Log "Initializing E2B Gateway environment" "INFO"
    
    # Set working directory
    if ($WorkingDirectory -and (Test-Path $WorkingDirectory)) {
        Set-Location $WorkingDirectory
        Write-Log "Working directory: $WorkingDirectory" "INFO"
    }
    
    # Check Python environment
    try {
        $pythonVersion = & python --version 2>$null
        Write-Log "Python environment: $pythonVersion" "INFO"
    } catch {
        Write-Log "Python not available in PATH" "WARN"
    }
    
    # Check Git availability
    try {
        $gitVersion = & git --version 2>$null
        Write-Log "Git environment: $gitVersion" "INFO"
    } catch {
        Write-Log "Git not available in PATH" "WARN"
    }
    
    # Check Node.js for additional tools
    try {
        $nodeVersion = & node --version 2>$null
        Write-Log "Node.js environment: $nodeVersion" "INFO"
    } catch {
        Write-Log "Node.js not available" "INFO"
    }
}

# Execute Omni Engine operations
function Invoke-OmniEngineOperation {
    param(
        [string]$Operation,
        [hashtable]$Config,
        [bool]$IsDryRun
    )
    
    if ($IsDryRun) {
        Write-Log "DRY RUN: Would execute: $Operation" "INFO"
        return @{success=$true; output="DRY RUN - Command not executed"; dry_run=$true}
    }
    
    # Security check
    if (-not (Test-CommandSecurity $Operation)) {
        Write-Log "Security violation detected in command: $Operation" "ERROR"
        return @{success=$false; error="Security violation"; blocked=$true}
    }
    
    try {
        Write-Log "Executing: $Operation" "INFO"
        
        $startTime = Get-Date
        
        # Execute command based on type
        if ($Operation.StartsWith("git ")) {
            # Git operations
            $result = Invoke-Expression $Operation 2>&1
        }
        elseif ($Operation.StartsWith("python ")) {
            # Python operations
            $result = Invoke-Expression $Operation 2>&1
        }
        elseif ($Operation.StartsWith("omni-")) {
            # Custom Omni Engine operations
            $result = Invoke-OmniCustomOperation $Operation $Config
        }
        else {
            # General operations
            $result = Invoke-Expression $Operation 2>&1
        }
        
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        
        Write-Log "Operation completed in $duration seconds" "INFO"
        
        return @{
            success = $true
            output = $result | Out-String
            duration = $duration
            timestamp = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
        }
        
    } catch {
        Write-Log "Operation failed: $($_.Exception.Message)" "ERROR"
        return @{
            success = $false
            error = $_.Exception.Message
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        }
    }
}

# Custom Omni Engine operations
function Invoke-OmniCustomOperation {
    param([string]$Operation, [hashtable]$Config)
    
    switch -Regex ($Operation) {
        "omni-status" {
            # Check Omni Engine status
            $status = @{
                omni_engine_version = "2.0.0-MCP"
                environment = $Environment
                working_directory = (Get-Location).Path
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                mcp_connectors_available = @(
                    "github_mcp", "gdrive_mcp", "e2b_mcp", "notion_mcp", "fileboss"
                )
            }
            return $status | ConvertTo-Json -Depth 3
        }
        
        "omni-test-connectors" {
            # Test MCP connector availability
            $connectorTests = @{}
            
            # Test Python dependencies
            try {
                & python -c "import httpx, json; print('HTTP client: OK')" 2>$null
                $connectorTests['http_client'] = 'OK'
            } catch {
                $connectorTests['http_client'] = 'FAILED'
            }
            
            try {
                & python -c "import notion_client; print('Notion: OK')" 2>$null
                $connectorTests['notion_client'] = 'OK'
            } catch {
                $connectorTests['notion_client'] = 'NOT_INSTALLED'
            }
            
            try {
                & python -c "import e2b; print('E2B: OK')" 2>$null
                $connectorTests['e2b_client'] = 'OK'
            } catch {
                $connectorTests['e2b_client'] = 'NOT_INSTALLED'
            }
            
            return $connectorTests | ConvertTo-Json
        }
        
        "omni-deploy" {
            # Deploy Omni Engine with MCP
            Write-Log "Deploying Omni Engine MCP configuration" "INFO"
            
            $deploySteps = @(
                "pip install -r requirements-mcp.txt",
                "python -m pytest tests/ -v",
                "python -m app.gui --mcp-enabled"
            )
            
            $deployResults = @{}
            foreach ($step in $deploySteps) {
                $stepResult = Invoke-Expression $step 2>&1
                $deployResults[$step] = $stepResult | Out-String
            }
            
            return $deployResults | ConvertTo-Json -Depth 2
        }
        
        "omni-intelligence" {
            # Run intelligence gathering
            Write-Log "Executing MCP intelligence gathering" "INFO"
            
            $intelligenceScript = @"
import sys
sys.path.append('.')
from modules.mcp_orchestrator import MCPOrchestrator, MCPConfiguration
from modules.memory_bridge import MemoryBridge

# Initialize MCP orchestrator
config = MCPConfiguration(
    fileboss_enabled=True,
    github_enabled=True,
    github_repositories=['GlacierEQ/Omni_Engine', 'GlacierEQ/FILEBOSS']
)

memory_bridge = MemoryBridge()
orchestrator = MCPOrchestrator(config=config, memory_bridge=memory_bridge)

# Execute intelligence gathering
results = orchestrator.execute_orchestrated_intelligence_gathering()
print(f"INTELLIGENCE_RESULT: {results}")
"@
            
            $tempScript = [System.IO.Path]::GetTempFileName() + ".py"
            $intelligenceScript | Out-File -FilePath $tempScript -Encoding UTF8
            
            try {
                $result = & python $tempScript 2>&1
                Remove-Item $tempScript -ErrorAction SilentlyContinue
                return $result | Out-String
            } catch {
                Remove-Item $tempScript -ErrorAction SilentlyContinue
                throw
            }
        }
        
        default {
            throw "Unknown Omni Engine operation: $Operation"
        }
    }
}

# Main execution
try {
    Write-Log "E2B Gateway starting - Command: $Cmd" "INFO"
    
    # Load configuration
    $config = Get-MCPConfig $MCPConfig
    
    # Initialize environment
    Initialize-Environment $config
    
    # Execute operation
    $result = Invoke-OmniEngineOperation $Cmd $config $DryRun
    
    # Output results
    if ($result.success) {
        Write-Log "Operation completed successfully" "INFO"
        if ($result.output) {
            Write-Output $result.output
        }
        exit 0
    } else {
        Write-Log "Operation failed: $($result.error)" "ERROR"
        Write-Error $result.error
        exit 1
    }
    
} catch {
    Write-Log "E2B Gateway error: $($_.Exception.Message)" "ERROR"
    Write-Error "E2B Gateway failed: $($_.Exception.Message)"
    exit 1
}

# Usage Examples:
# .\.\e2b_gateway.ps1 -Cmd "git status" -Verbose
# .\.\e2b_gateway.ps1 -Cmd "omni-status" -Environment production
# .\.\e2b_gateway.ps1 -Cmd "omni-intelligence" -Verbose
# .\.\e2b_gateway.ps1 -Cmd "python -m app.gui" -DryRun
