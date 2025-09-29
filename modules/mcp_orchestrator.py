"""MCP (Maximum Control Point) Orchestrator for unified connector management."""

from __future__ import annotations

import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from .connectors import (
    Connector,
    FileBossConnector,
    MegaPdfConnector,
    WhisperXConnector
)

# Import new MCP connectors
try:
    from .connectors.github_mcp import GitHubMCPConnector
except ImportError:
    GitHubMCPConnector = None

try:
    from .connectors.gdrive_mcp import GoogleDriveMCPConnector
except ImportError:
    GoogleDriveMCPConnector = None

try:
    from .connectors.e2b_mcp import E2BMCPConnector
except ImportError:
    E2BMCPConnector = None

try:
    from .connectors.notion_mcp import NotionMCPConnector
except ImportError:
    NotionMCPConnector = None

from .memory_bridge import MemoryBridge, MemoryEntry
from .operator import OperatorCore

logger = logging.getLogger(__name__)


@dataclass
class MCPConfiguration:
    """Configuration for MCP connectors."""
    
    # GitHub MCP Configuration
    github_enabled: bool = False
    github_token: str = ""
    github_repositories: List[str] = field(default_factory=list)
    
    # Google Drive MCP Configuration  
    gdrive_enabled: bool = False
    gdrive_credentials_path: str = ""
    gdrive_folder_ids: List[str] = field(default_factory=list)
    
    # E2B MCP Configuration
    e2b_enabled: bool = False
    e2b_api_key: str = ""
    e2b_template: str = "base"
    
    # Notion MCP Configuration
    notion_enabled: bool = False
    notion_api_token: str = ""
    notion_database_ids: List[str] = field(default_factory=list)
    notion_page_ids: List[str] = field(default_factory=list)
    
    # FILEBOSS Integration
    fileboss_enabled: bool = True
    fileboss_root_path: str = "./data/fileboss"
    
    # General MCP Settings
    parallel_execution: bool = True
    max_workers: int = 4
    timeout_seconds: int = 300
    memory_layers: List[str] = field(default_factory=lambda: [
        "legal_evidence",
        "github_intelligence", 
        "cloud_evidence",
        "ai_execution",
        "knowledge_base"
    ])


@dataclass
class MCPOrchestrator:
    """Maximum Control Point orchestrator for unified connector management.
    
    Coordinates multiple MCP connectors, manages memory integration,
    and provides comprehensive intelligence gathering for legal cases.
    """
    
    config: MCPConfiguration
    memory_bridge: MemoryBridge
    operator_core: Optional[OperatorCore] = None
    
    def __post_init__(self):
        self.connectors: Dict[str, Connector] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.last_execution: Optional[datetime] = None
        
        # Initialize connectors based on configuration
        self._initialize_connectors()
        
        logger.info(f"MCP Orchestrator initialized with {len(self.connectors)} connectors")
    
    def _initialize_connectors(self) -> None:
        """Initialize all enabled MCP connectors."""
        
        # Initialize FILEBOSS connector
        if self.config.fileboss_enabled:
            try:
                fileboss_path = Path(self.config.fileboss_root_path)
                fileboss_path.mkdir(parents=True, exist_ok=True)
                
                self.connectors["fileboss"] = FileBossConnector(
                    name="FILEBOSS_MCP",
                    root=fileboss_path,
                    layer="legal_evidence"
                )
                logger.info("FILEBOSS MCP connector initialized")
            except Exception as e:
                logger.error(f"Failed to initialize FILEBOSS connector: {e}")
        
        # Initialize GitHub MCP connector
        if self.config.github_enabled and GitHubMCPConnector:
            try:
                self.connectors["github"] = GitHubMCPConnector(
                    name="GitHub_Intelligence",
                    github_token=self.config.github_token,
                    repositories=self.config.github_repositories,
                    layer="github_intelligence"
                )
                logger.info("GitHub MCP connector initialized")
            except Exception as e:
                logger.error(f"Failed to initialize GitHub MCP connector: {e}")
        
        # Initialize Google Drive MCP connector
        if self.config.gdrive_enabled and GoogleDriveMCPConnector:
            try:
                self.connectors["gdrive"] = GoogleDriveMCPConnector(
                    name="GDrive_Evidence",
                    credentials_path=self.config.gdrive_credentials_path,
                    folder_ids=self.config.gdrive_folder_ids,
                    layer="cloud_evidence"
                )
                logger.info("Google Drive MCP connector initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Drive MCP connector: {e}")
        
        # Initialize E2B MCP connector
        if self.config.e2b_enabled and E2BMCPConnector:
            try:
                self.connectors["e2b"] = E2BMCPConnector(
                    name="E2B_Sandbox",
                    api_key=self.config.e2b_api_key,
                    template=self.config.e2b_template,
                    layer="ai_execution"
                )
                logger.info("E2B MCP connector initialized")
            except Exception as e:
                logger.error(f"Failed to initialize E2B MCP connector: {e}")
        
        # Initialize Notion MCP connector
        if self.config.notion_enabled and NotionMCPConnector:
            try:
                self.connectors["notion"] = NotionMCPConnector(
                    name="Notion_Knowledge",
                    api_token=self.config.notion_api_token,
                    database_ids=self.config.notion_database_ids,
                    page_ids=self.config.notion_page_ids,
                    layer="knowledge_base"
                )
                logger.info("Notion MCP connector initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Notion MCP connector: {e}")
    
    def add_connector(self, name: str, connector: Connector) -> None:
        """Add a custom connector to the orchestrator."""
        self.connectors[name] = connector
        logger.info(f"Added custom connector: {name}")
    
    def remove_connector(self, name: str) -> bool:
        """Remove a connector from the orchestrator."""
        if name in self.connectors:
            del self.connectors[name]
            logger.info(f"Removed connector: {name}")
            return True
        return False
    
    def get_connector_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status information for all connectors."""
        status = {}
        
        for name, connector in self.connectors.items():
            try:
                status[name] = {
                    "name": connector.name,
                    "layer": getattr(connector, 'layer', 'unknown'),
                    "source": getattr(connector, 'source', 'unknown'),
                    "type": type(connector).__name__,
                    "enabled": True
                }
            except Exception as e:
                status[name] = {
                    "error": str(e),
                    "enabled": False
                }
        
        return status
    
    def execute_single_connector(self, connector_name: str) -> List[MemoryEntry]:
        """Execute a single connector and return its results."""
        if connector_name not in self.connectors:
            logger.error(f"Connector {connector_name} not found")
            return []
        
        connector = self.connectors[connector_name]
        
        try:
            logger.info(f"Executing connector: {connector_name}")
            start_time = datetime.now()
            
            entries = list(connector.gather())
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Log execution history
            self.execution_history.append({
                "connector": connector_name,
                "timestamp": start_time.isoformat(),
                "execution_time": execution_time,
                "entries_generated": len(entries),
                "success": True
            })
            
            logger.info(f"Connector {connector_name} generated {len(entries)} entries in {execution_time:.2f}s")
            return entries
            
        except Exception as e:
            logger.error(f"Connector {connector_name} execution failed: {e}")
            
            # Log failed execution
            self.execution_history.append({
                "connector": connector_name,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            })
            
            return []
    
    def execute_parallel(self) -> Dict[str, List[MemoryEntry]]:
        """Execute all connectors in parallel."""
        results = {}
        
        if not self.config.parallel_execution or len(self.connectors) <= 1:
            # Sequential execution
            for name in self.connectors:
                results[name] = self.execute_single_connector(name)
        else:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                future_to_connector = {
                    executor.submit(self.execute_single_connector, name): name
                    for name in self.connectors
                }
                
                for future in as_completed(future_to_connector, timeout=self.config.timeout_seconds):
                    connector_name = future_to_connector[future]
                    try:
                        results[connector_name] = future.result()
                    except Exception as e:
                        logger.error(f"Parallel execution failed for {connector_name}: {e}")
                        results[connector_name] = []
        
        return results
    
    def execute_orchestrated_intelligence_gathering(self) -> Dict[str, Any]:
        """Execute comprehensive intelligence gathering across all connectors."""
        start_time = datetime.now()
        logger.info("Starting orchestrated intelligence gathering")
        
        # Execute all connectors
        connector_results = self.execute_parallel()
        
        # Aggregate results
        all_entries = []
        connector_summary = {}
        
        for connector_name, entries in connector_results.items():
            all_entries.extend(entries)
            connector_summary[connector_name] = {
                "entries_count": len(entries),
                "layers": list(set(entry.layer for entry in entries)),
                "sources": list(set(entry.source for entry in entries))
            }
        
        # Integrate with memory bridge
        memory_integration_success = False
        try:
            for entry in all_entries:
                self.memory_bridge.add_entry(entry)
            memory_integration_success = True
            logger.info(f"Integrated {len(all_entries)} entries into memory bridge")
        except Exception as e:
            logger.error(f"Memory bridge integration failed: {e}")
        
        # Generate orchestration summary
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        orchestration_summary = {
            "execution_timestamp": start_time.isoformat(),
            "total_execution_time": execution_time,
            "connectors_executed": list(connector_results.keys()),
            "total_entries_generated": len(all_entries),
            "memory_integration_success": memory_integration_success,
            "connector_summary": connector_summary,
            "layer_distribution": {},
            "source_distribution": {}
        }
        
        # Analyze layer and source distribution
        for entry in all_entries:
            layer = entry.layer
            source = entry.source
            
            orchestration_summary["layer_distribution"][layer] = \
                orchestration_summary["layer_distribution"].get(layer, 0) + 1
            orchestration_summary["source_distribution"][source] = \
                orchestration_summary["source_distribution"].get(source, 0) + 1
        
        # Update execution tracking
        self.last_execution = start_time
        
        # Integrate with operator core if available
        if self.operator_core:
            try:
                # Generate operational recommendations
                recommendations = self._generate_operational_recommendations(
                    orchestration_summary, all_entries
                )
                orchestration_summary["operational_recommendations"] = recommendations
            except Exception as e:
                logger.error(f"Failed to generate operational recommendations: {e}")
        
        logger.info(f"Orchestrated intelligence gathering completed in {execution_time:.2f}s")
        return orchestration_summary
    
    def _generate_operational_recommendations(self, summary: Dict[str, Any], entries: List[MemoryEntry]) -> List[str]:
        """Generate operational recommendations based on gathered intelligence."""
        recommendations = []
        
        # Check for data quality issues
        if summary["total_entries_generated"] == 0:
            recommendations.append("No intelligence entries generated - check connector configurations")
        elif summary["total_entries_generated"] < 10:
            recommendations.append("Low intelligence yield - consider expanding data sources")
        
        # Check connector performance
        failed_connectors = []
        for conn_name, conn_data in summary["connector_summary"].items():
            if conn_data["entries_count"] == 0:
                failed_connectors.append(conn_name)
        
        if failed_connectors:
            recommendations.append(f"Connectors with no output: {', '.join(failed_connectors)}")
        
        # Check memory integration
        if not summary.get("memory_integration_success"):
            recommendations.append("Memory bridge integration failed - manual intervention required")
        
        # Analyze content patterns for legal relevance
        evidence_keywords = ['evidence', 'legal', 'case', 'court', 'lawsuit', 'litigation']
        relevant_entries = 0
        
        for entry in entries:
            content_lower = entry.content.lower()
            if any(keyword in content_lower for keyword in evidence_keywords):
                relevant_entries += 1
        
        if relevant_entries == 0:
            recommendations.append("No legal-relevant content detected - verify case materials are being processed")
        elif relevant_entries < len(entries) * 0.3:  # Less than 30% relevant
            recommendations.append("Low legal relevance in gathered intelligence - refine data sources")
        
        # Performance recommendations
        if summary["total_execution_time"] > 300:  # 5 minutes
            recommendations.append("Long execution time detected - consider optimizing connector configurations")
        
        return recommendations
    
    def get_orchestration_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics about orchestrator performance."""
        metrics = {
            "total_connectors": len(self.connectors),
            "enabled_connectors": list(self.connectors.keys()),
            "total_executions": len(self.execution_history),
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "execution_history": self.execution_history[-10:],  # Last 10 executions
            "memory_layers": self.config.memory_layers,
            "configuration": {
                "parallel_execution": self.config.parallel_execution,
                "max_workers": self.config.max_workers,
                "timeout_seconds": self.config.timeout_seconds
            }
        }
        
        # Calculate success rate
        if self.execution_history:
            successful_executions = sum(1 for exec in self.execution_history if exec.get("success", False))
            metrics["success_rate"] = successful_executions / len(self.execution_history)
        else:
            metrics["success_rate"] = 0.0
        
        return metrics
    
    def export_configuration(self, file_path: Path) -> None:
        """Export current configuration to JSON file."""
        config_data = {
            "mcp_configuration": {
                "github_enabled": self.config.github_enabled,
                "gdrive_enabled": self.config.gdrive_enabled,
                "e2b_enabled": self.config.e2b_enabled,
                "notion_enabled": self.config.notion_enabled,
                "fileboss_enabled": self.config.fileboss_enabled,
                "parallel_execution": self.config.parallel_execution,
                "max_workers": self.config.max_workers,
                "timeout_seconds": self.config.timeout_seconds,
                "memory_layers": self.config.memory_layers
            },
            "connector_status": self.get_connector_status(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"Configuration exported to {file_path}")
    
    @classmethod
    def from_config_file(cls, config_path: Path, memory_bridge: MemoryBridge) -> 'MCPOrchestrator':
        """Create orchestrator from configuration file."""
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        mcp_config_data = config_data.get("mcp_configuration", {})
        
        config = MCPConfiguration(
            github_enabled=mcp_config_data.get("github_enabled", False),
            gdrive_enabled=mcp_config_data.get("gdrive_enabled", False),
            e2b_enabled=mcp_config_data.get("e2b_enabled", False),
            notion_enabled=mcp_config_data.get("notion_enabled", False),
            fileboss_enabled=mcp_config_data.get("fileboss_enabled", True),
            parallel_execution=mcp_config_data.get("parallel_execution", True),
            max_workers=mcp_config_data.get("max_workers", 4),
            timeout_seconds=mcp_config_data.get("timeout_seconds", 300),
            memory_layers=mcp_config_data.get("memory_layers", [
                "legal_evidence", "github_intelligence", "cloud_evidence", 
                "ai_execution", "knowledge_base"
            ])
        )
        
        return cls(config=config, memory_bridge=memory_bridge)


__all__ = ["MCPOrchestrator", "MCPConfiguration"]
