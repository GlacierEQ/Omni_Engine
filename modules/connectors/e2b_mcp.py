"""E2B MCP (Maximum Control Point) Connector for secure AI sandbox execution."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

try:
    from e2b import Sandbox
except ImportError:
    logging.warning("E2B dependencies not installed. Install with: pip install e2b")
    Sandbox = None

from ..memory_bridge import MemoryEntry
from . import Connector

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class E2BMCPConnector(Connector):
    """Maximum Control Point connector for E2B AI sandbox execution.
    
    Provides secure code execution, file processing, and automated analysis
    within isolated sandbox environments for legal evidence processing.
    """

    name: str
    api_key: str
    template: str = "base"  # E2B template to use
    layer: str = "ai_execution"
    source: str = "E2B_MCP"
    timeout: int = 300  # 5 minutes default timeout
    max_executions: int = 10
    auto_cleanup: bool = True
    working_directory: str = "/tmp/omni_engine"
    execution_scripts: List[Dict[str, str]] = field(default_factory=list)
    file_analysis_enabled: bool = True
    code_analysis_enabled: bool = True
    memory_integration: bool = True
    
    def __post_init__(self):
        if not Sandbox:
            raise ImportError("E2B package not installed. Install with: pip install e2b")
        
        if not self.api_key:
            self.api_key = os.getenv('E2B_API_KEY')
            if not self.api_key:
                raise ValueError("E2B API key not provided and E2B_API_KEY environment variable not set")
        
        self.execution_count = 0
        self.sandbox_sessions = []

    def _create_sandbox(self) -> Sandbox:
        """Create a new E2B sandbox instance."""
        try:
            sandbox = Sandbox(
                template=self.template,
                api_key=self.api_key,
                timeout=self.timeout
            )
            
            # Setup working directory
            sandbox.filesystem.make_dir(self.working_directory)
            
            logger.info(f"Created E2B sandbox with ID: {sandbox.id}")
            self.sandbox_sessions.append(sandbox)
            return sandbox
            
        except Exception as e:
            logger.error(f"Failed to create E2B sandbox: {e}")
            raise

    def _execute_code(self, sandbox: Sandbox, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in the sandbox and return results."""
        try:
            start_time = datetime.now()
            
            if language.lower() == "python":
                result = sandbox.run_code(code)
            elif language.lower() == "bash" or language.lower() == "shell":
                result = sandbox.terminal.run(code)
            else:
                raise ValueError(f"Unsupported language: {language}")
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            return {
                "success": True,
                "stdout": result.stdout if hasattr(result, 'stdout') else str(result),
                "stderr": result.stderr if hasattr(result, 'stderr') else "",
                "exit_code": getattr(result, 'exit_code', 0),
                "execution_time": execution_time,
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _analyze_file_with_ai(self, sandbox: Sandbox, file_path: str) -> Dict[str, Any]:
        """Analyze a file using AI capabilities in the sandbox."""
        analysis_code = f"""
import os
import mimetypes
import hashlib
from pathlib import Path

file_path = "{file_path}"
result = {{}}

# Basic file information
if os.path.exists(file_path):
    stat = os.stat(file_path)
    result['exists'] = True
    result['size'] = stat.st_size
    result['modified_time'] = stat.st_mtime
    result['mime_type'] = mimetypes.guess_type(file_path)[0]
    
    # Calculate file hash
    with open(file_path, 'rb') as f:
        content = f.read()
        result['md5_hash'] = hashlib.md5(content).hexdigest()
        result['sha256_hash'] = hashlib.sha256(content).hexdigest()
    
    # Content analysis based on file type
    if result['mime_type'] and 'text' in result['mime_type']:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text_content = f.read()
            result['content_preview'] = text_content[:1000]  # First 1000 chars
            result['line_count'] = len(text_content.splitlines())
            result['word_count'] = len(text_content.split())
    
    elif result['mime_type'] == 'application/pdf':
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                result['page_count'] = len(pdf_reader.pages)
                if pdf_reader.pages:
                    result['first_page_text'] = pdf_reader.pages[0].extract_text()[:500]
        except ImportError:
            result['pdf_analysis'] = 'PyPDF2 not available'
        except Exception as e:
            result['pdf_error'] = str(e)
else:
    result['exists'] = False

print(f"ANALYSIS_RESULT: {{result}}")
"""
        
        execution_result = self._execute_code(sandbox, analysis_code, "python")
        
        # Extract analysis result from output
        analysis = {"basic_execution": execution_result}
        
        if execution_result.get("success") and "ANALYSIS_RESULT:" in execution_result.get("stdout", ""):
            try:
                output_lines = execution_result["stdout"].split("\n")
                for line in output_lines:
                    if "ANALYSIS_RESULT:" in line:
                        result_str = line.split("ANALYSIS_RESULT:", 1)[1].strip()
                        analysis["file_analysis"] = eval(result_str)  # Note: eval is risky but controlled environment
                        break
            except Exception as e:
                logger.error(f"Failed to parse analysis result: {e}")
                analysis["parse_error"] = str(e)
        
        return analysis

    def _run_legal_analysis_scripts(self, sandbox: Sandbox) -> List[Dict[str, Any]]:
        """Run legal-specific analysis scripts in the sandbox."""
        results = []
        
        # Default legal analysis scripts
        legal_scripts = [
            {
                "name": "evidence_metadata_extractor",
                "language": "python",
                "code": """
# Evidence Metadata Extraction
import os
import json
from datetime import datetime

metadata = {
    'analysis_type': 'evidence_metadata',
    'timestamp': datetime.now().isoformat(),
    'working_directory': os.getcwd(),
    'file_list': [],
    'environment_info': {
        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
        'platform': os.name,
        'available_modules': []
    }
}

# List files in working directory
for root, dirs, files in os.walk('.'):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            stat = os.stat(file_path)
            metadata['file_list'].append({
                'path': file_path,
                'size': stat.st_size,
                'modified': stat.st_mtime
            })
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

print(f"METADATA_RESULT: {json.dumps(metadata)}")
"""
            },
            {
                "name": "system_forensics_check",
                "language": "bash",
                "code": """
# System Forensics Information
echo "=== SYSTEM FORENSICS REPORT ==="
echo "Timestamp: $(date)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"
echo "Disk Usage:"
df -h | head -5
echo "Memory Info:"
free -h 2>/dev/null || echo "Memory info not available"
echo "Process Count: $(ps aux | wc -l)"
echo "Network Interfaces:"
ip addr show 2>/dev/null | grep -E '^[0-9]+:' || ifconfig -a 2>/dev/null | grep -E '^[a-z0-9]+:' || echo "Network info not available"
"""
            }
        ]
        
        # Add custom scripts
        all_scripts = legal_scripts + self.execution_scripts
        
        for script in all_scripts:
            try:
                result = self._execute_code(
                    sandbox,
                    script["code"],
                    script.get("language", "python")
                )
                
                script_result = {
                    "script_name": script["name"],
                    "language": script.get("language", "python"),
                    "execution_result": result
                }
                
                results.append(script_result)
                
            except Exception as e:
                logger.error(f"Failed to execute script {script['name']}: {e}")
                results.append({
                    "script_name": script["name"],
                    "error": str(e)
                })
        
        return results

    def _process_fileboss_integration(self, sandbox: Sandbox) -> Dict[str, Any]:
        """Process FILEBOSS files within the sandbox environment."""
        fileboss_code = """
import os
import json
from pathlib import Path

# FILEBOSS Integration Analysis
fileboss_analysis = {
    'integration_type': 'fileboss_mcp',
    'case_files_processed': 0,
    'evidence_items': [],
    'processing_errors': []
}

# Look for FILEBOSS data patterns
data_patterns = ['*.pdf', '*.docx', '*.txt', '*.csv', '*.json']
for pattern in data_patterns:
    try:
        import glob
        files = glob.glob(f"**/{pattern}", recursive=True)
        for file_path in files:
            try:
                stat = os.stat(file_path)
                evidence_item = {
                    'file_path': file_path,
                    'size': stat.st_size,
                    'modified_time': stat.st_mtime,
                    'pattern_match': pattern
                }
                fileboss_analysis['evidence_items'].append(evidence_item)
                fileboss_analysis['case_files_processed'] += 1
            except Exception as e:
                fileboss_analysis['processing_errors'].append(f"Error processing {file_path}: {e}")
    except Exception as e:
        fileboss_analysis['processing_errors'].append(f"Pattern {pattern} failed: {e}")

print(f"FILEBOSS_RESULT: {json.dumps(fileboss_analysis)}")
"""
        
        result = self._execute_code(sandbox, fileboss_code, "python")
        
        # Parse FILEBOSS result
        fileboss_data = {"execution": result}
        if result.get("success") and "FILEBOSS_RESULT:" in result.get("stdout", ""):
            try:
                output_lines = result["stdout"].split("\n")
                for line in output_lines:
                    if "FILEBOSS_RESULT:" in line:
                        result_str = line.split("FILEBOSS_RESULT:", 1)[1].strip()
                        fileboss_data["analysis"] = json.loads(result_str)
                        break
            except Exception as e:
                logger.error(f"Failed to parse FILEBOSS result: {e}")
                fileboss_data["parse_error"] = str(e)
        
        return fileboss_data

    def gather(self) -> Iterable[MemoryEntry]:
        """Gather E2B sandbox execution intelligence and results."""
        entries = []
        
        try:
            # Create sandbox
            sandbox = self._create_sandbox()
            
            # Sandbox initialization info
            init_info = {
                "sandbox_id": sandbox.id,
                "template": self.template,
                "working_directory": self.working_directory,
                "timeout": self.timeout,
                "timestamp": datetime.now().isoformat()
            }
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"E2B Sandbox Initialized\n{json.dumps(init_info, indent=2)}",
                source=f"{self.source}_INIT",
                metadata={"sandbox_id": sandbox.id, "analysis_type": "initialization"}
            ))
            
            # Run legal analysis scripts
            if self.code_analysis_enabled:
                script_results = self._run_legal_analysis_scripts(sandbox)
                
                for script_result in script_results:
                    entries.append(MemoryEntry(
                        layer=self.layer,
                        content=f"E2B Script Execution: {script_result['script_name']}\n{json.dumps(script_result, indent=2, default=str)}",
                        source=f"{self.source}_SCRIPT",
                        metadata={
                            "sandbox_id": sandbox.id,
                            "script_name": script_result['script_name'],
                            "analysis_type": "script_execution"
                        }
                    ))
            
            # FILEBOSS integration processing
            if self.memory_integration:
                fileboss_result = self._process_fileboss_integration(sandbox)
                
                entries.append(MemoryEntry(
                    layer=self.layer,
                    content=f"E2B FILEBOSS Integration\n{json.dumps(fileboss_result, indent=2, default=str)}",
                    source=f"{self.source}_FILEBOSS",
                    metadata={
                        "sandbox_id": sandbox.id,
                        "analysis_type": "fileboss_integration"
                    }
                ))
            
            # Sandbox summary
            summary = {
                "sandbox_id": sandbox.id,
                "execution_count": len(script_results) if 'script_results' in locals() else 0,
                "total_entries_generated": len(entries),
                "session_duration": "active",
                "final_timestamp": datetime.now().isoformat()
            }
            
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"E2B Session Summary\n{json.dumps(summary, indent=2)}",
                source=f"{self.source}_SUMMARY",
                metadata={"sandbox_id": sandbox.id, "analysis_type": "summary"}
            ))
            
        except Exception as e:
            logger.error(f"E2B sandbox execution failed: {e}")
            entries.append(MemoryEntry(
                layer=self.layer,
                content=f"E2B Execution Error: {str(e)}",
                source=f"{self.source}_ERROR",
                metadata={"analysis_type": "error"}
            ))
        
        finally:
            # Cleanup sandboxes if auto_cleanup is enabled
            if self.auto_cleanup:
                for sandbox in self.sandbox_sessions:
                    try:
                        sandbox.close()
                        logger.info(f"Closed sandbox {sandbox.id}")
                    except Exception as e:
                        logger.error(f"Failed to close sandbox {sandbox.id}: {e}")
                self.sandbox_sessions.clear()
        
        logger.info(f"E2B MCP generated {len(entries)} execution entries")
        return entries

    def execute_custom_analysis(self, code: str, language: str = "python") -> MemoryEntry:
        """Execute custom analysis code and return as memory entry."""
        try:
            sandbox = self._create_sandbox()
            result = self._execute_code(sandbox, code, language)
            
            analysis = {
                "type": "custom_execution",
                "language": language,
                "code_preview": code[:200] + "..." if len(code) > 200 else code,
                "execution_result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            if self.auto_cleanup:
                sandbox.close()
            
            return MemoryEntry(
                layer=self.layer,
                content=f"E2B Custom Analysis\n{json.dumps(analysis, indent=2, default=str)}",
                source=f"{self.source}_CUSTOM",
                metadata={"analysis_type": "custom_execution", "language": language}
            )
            
        except Exception as e:
            logger.error(f"Custom execution failed: {e}")
            return MemoryEntry(
                layer=self.layer,
                content=f"E2B Custom Execution Error: {str(e)}",
                source=f"{self.source}_CUSTOM_ERROR",
                metadata={"analysis_type": "custom_error"}
            )


__all__ = ["E2BMCPConnector"]
