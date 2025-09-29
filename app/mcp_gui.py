"""MCP-Enhanced GUI for Omni Engine with real-time intelligence dashboard."""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Button, DataTable, Footer, Header, Input, Label, 
    ProgressBar, RichLog, Static, Switch, TabbedContent, TabPane, Tree
)
from textual.reactive import reactive
from textual.message import Message
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import Omni Engine modules
import sys
sys.path.append('..')

try:
    from modules.mcp_orchestrator import MCPOrchestrator, MCPConfiguration
    from modules.memory_bridge import MemoryBridge
    from modules.legal_intelligence_analyzer import LegalIntelligenceAnalyzer
except ImportError as e:
    logging.error(f"Failed to import Omni Engine modules: {e}")
    MCPOrchestrator = MCPConfiguration = MemoryBridge = LegalIntelligenceAnalyzer = None

logger = logging.getLogger(__name__)


class MCPStatusWidget(Static):
    """Widget displaying MCP connector status."""
    
    def __init__(self, orchestrator: Optional[MCPOrchestrator] = None):
        super().__init__()
        self.orchestrator = orchestrator
        self.update_timer = None
    
    def compose(self) -> ComposeResult:
        yield Label("MCP Connector Status", classes="header")
        yield RichLog(id="mcp_status_log", auto_scroll=True)
    
    def on_mount(self) -> None:
        self.update_status()
        # Auto-update every 30 seconds
        self.update_timer = self.set_interval(30, self.update_status)
    
    def update_status(self) -> None:
        log = self.query_one("#mcp_status_log", RichLog)
        
        if not self.orchestrator:
            log.write("[red]MCP Orchestrator not initialized[/red]")
            return
        
        try:
            status = self.orchestrator.get_connector_status()
            
            table = Table(title="MCP Connector Status", show_header=True)
            table.add_column("Connector", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Layer", style="yellow")
            table.add_column("Source", style="magenta")
            
            for conn_name, conn_data in status.items():
                status_text = "✅ ENABLED" if conn_data.get("enabled") else "❌ DISABLED"
                if "error" in conn_data:
                    status_text = f"⚠️ ERROR: {conn_data['error'][:30]}..."
                
                table.add_row(
                    conn_name,
                    status_text,
                    conn_data.get("layer", "unknown"),
                    conn_data.get("source", "unknown")
                )
            
            log.write(table)
            
        except Exception as e:
            log.write(f"[red]Status update failed: {e}[/red]")


class IntelligenceWidget(Static):
    """Widget for displaying intelligence gathering results."""
    
    intelligence_data: reactive[Dict] = reactive({})
    
    def compose(self) -> ComposeResult:
        yield Label("Intelligence Dashboard", classes="header")
        with TabbedContent():
            with TabPane("Overview", id="overview_tab"):
                yield RichLog(id="overview_log", auto_scroll=True)
            with TabPane("Entities", id="entities_tab"):
                yield DataTable(id="entities_table")
            with TabPane("Timeline", id="timeline_tab"):
                yield DataTable(id="timeline_table")
            with TabPane("Patterns", id="patterns_tab"):
                yield RichLog(id="patterns_log")
            with TabPane("Risks", id="risks_tab"):
                yield RichLog(id="risks_log")
    
    def watch_intelligence_data(self, data: Dict) -> None:
        """React to intelligence data updates."""
        if not data:
            return
        
        self.update_overview(data)
        self.update_entities(data)
        self.update_timeline(data) 
        self.update_patterns(data)
        self.update_risks(data)
    
    def update_overview(self, data: Dict) -> None:
        log = self.query_one("#overview_log", RichLog)
        
        metadata = data.get("analysis_metadata", {})
        entity_analysis = data.get("entity_analysis", {})
        timeline_analysis = data.get("timeline_analysis", {})
        
        overview_table = Table(title="Intelligence Overview", show_header=True)
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Value", style="yellow")
        
        overview_table.add_row("Case Number", metadata.get("case_number", "Unknown"))
        overview_table.add_row("Analysis Time", f"{metadata.get('analysis_duration', 0):.2f}s")
        overview_table.add_row("Entries Analyzed", str(metadata.get("entries_analyzed", 0)))
        overview_table.add_row("Total Entities", str(entity_analysis.get("total_entities", 0)))
        overview_table.add_row("Timeline Events", str(timeline_analysis.get("total_events", 0)))
        overview_table.add_row("Critical Events", str(timeline_analysis.get("critical_events", 0)))
        
        log.write(overview_table)
    
    def update_entities(self, data: Dict) -> None:
        table = self.query_one("#entities_table", DataTable)
        table.clear(columns=True)
        
        table.add_columns("Type", "Count", "High Confidence")
        
        entity_data = data.get("entities", {})
        for entity_type, entities in entity_data.items():
            high_conf_count = sum(1 for e in entities if e.get("confidence", 0) > 0.8)
            table.add_row(
                entity_type.title(),
                str(len(entities)),
                str(high_conf_count)
            )
    
    def update_timeline(self, data: Dict) -> None:
        table = self.query_one("#timeline_table", DataTable)
        table.clear(columns=True)
        
        table.add_columns("Date", "Event Type", "Significance", "Description")
        
        timeline_data = data.get("timeline", [])
        for event in timeline_data[-20:]:  # Show last 20 events
            table.add_row(
                event.get("date", "")[:10],  # Date only
                event.get("event_type", "unknown").title(),
                event.get("significance", "medium").upper(),
                event.get("description", "")[:50] + "..."
            )
    
    def update_patterns(self, data: Dict) -> None:
        log = self.query_one("#patterns_log", RichLog)
        
        patterns = data.get("patterns", [])
        
        if patterns:
            pattern_table = Table(title="Legal Patterns Identified", show_header=True)
            pattern_table.add_column("Pattern Type", style="cyan")
            pattern_table.add_column("Frequency", style="yellow")
            pattern_table.add_column("Confidence", style="green")
            pattern_table.add_column("Significance", style="red")
            
            for pattern in patterns:
                confidence_pct = f"{pattern.get('confidence', 0) * 100:.1f}%"
                pattern_table.add_row(
                    pattern.get("type", "unknown").replace("_", " ").title(),
                    str(pattern.get("frequency", 0)),
                    confidence_pct,
                    "High" if pattern.get("confidence", 0) > 0.8 else "Medium" if pattern.get("confidence", 0) > 0.5 else "Low"
                )
            
            log.write(pattern_table)
        else:
            log.write("[yellow]No significant patterns identified[/yellow]")
    
    def update_risks(self, data: Dict) -> None:
        log = self.query_one("#risks_log", RichLog)
        
        risk_data = data.get("risk_assessment", {})
        
        if risk_data:
            # Risk level panel
            risk_level = risk_data.get("overall_risk_level", "unknown")
            risk_color = {
                "critical": "red",
                "high": "orange", 
                "medium": "yellow",
                "low": "green"
            }.get(risk_level, "white")
            
            risk_panel = Panel(
                f"Overall Risk Level: {risk_level.upper()}",
                style=risk_color,
                title="Risk Assessment"
            )
            log.write(risk_panel)
            
            # Risk factors
            risk_factors = risk_data.get("risk_factors", [])
            if risk_factors:
                factors_table = Table(title="Risk Factors", show_header=True)
                factors_table.add_column("Risk Type", style="red")
                factors_table.add_column("Severity", style="orange")
                factors_table.add_column("Indicators", style="yellow")
                
                for factor in risk_factors:
                    factors_table.add_row(
                        factor.get("type", "unknown").replace("_", " ").title(),
                        factor.get("severity", "unknown").upper(),
                        str(factor.get("indicators_found", 0))
                    )
                
                log.write(factors_table)
            
            # Opportunities
            opportunities = risk_data.get("opportunities", [])
            if opportunities:
                opp_table = Table(title="Opportunities", show_header=True)
                opp_table.add_column("Opportunity Type", style="green")
                opp_table.add_column("Potential", style="cyan")
                opp_table.add_column("Indicators", style="yellow")
                
                for opp in opportunities:
                    opp_table.add_row(
                        opp.get("type", "unknown").replace("_", " ").title(),
                        opp.get("potential", "unknown").upper(),
                        str(opp.get("indicators_found", 0))
                    )
                
                log.write(opp_table)
        
        # Strategic recommendations
        recommendations = data.get("strategic_recommendations", [])
        if recommendations:
            log.write("[bold cyan]Strategic Recommendations:[/bold cyan]")
            for i, rec in enumerate(recommendations, 1):
                log.write(f"[green]{i}.[/green] {rec}")


class OmniEngineMCPApp(App):
    """Enhanced Omni Engine MCP application with comprehensive intelligence dashboard."""
    
    CSS = """
    .header {
        text-align: center;
        color: cyan;
        text-style: bold;
    }
    
    #control_panel {
        dock: left;
        width: 30;
        background: $surface;
    }
    
    #main_dashboard {
        dock: right;
        background: $background;
    }
    
    #status_bar {
        dock: bottom;
        height: 1;
        background: $accent;
    }
    
    Button {
        margin: 1;
    }
    
    DataTable {
        height: 15;
    }
    
    RichLog {
        height: 20;
        border: solid $primary;
    }
    """
    
    def __init__(self, config_path: str = "mcp_config.json"):
        super().__init__()
        self.config_path = config_path
        self.orchestrator: Optional[MCPOrchestrator] = None
        self.memory_bridge: Optional[MemoryBridge] = None
        self.legal_analyzer: Optional[LegalIntelligenceAnalyzer] = None
        self.intelligence_widget: Optional[IntelligenceWidget] = None
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self) -> None:
        """Load MCP configuration from file."""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config_data = json.load(f)
                
                # Initialize memory bridge
                self.memory_bridge = MemoryBridge()
                
                # Initialize orchestrator
                if MCPOrchestrator and MCPConfiguration:
                    mcp_config_data = config_data.get("mcp_configuration", {})
                    connectors_config = mcp_config_data.get("connectors", {})
                    
                    config = MCPConfiguration(
                        github_enabled=connectors_config.get("github_mcp", {}).get("enabled", False),
                        github_token=os.getenv('GITHUB_TOKEN', ''),
                        github_repositories=connectors_config.get("github_mcp", {}).get("repositories", []),
                        gdrive_enabled=connectors_config.get("gdrive_mcp", {}).get("enabled", False),
                        gdrive_credentials_path=connectors_config.get("gdrive_mcp", {}).get("credentials_path", ""),
                        e2b_enabled=connectors_config.get("e2b_mcp", {}).get("enabled", False),
                        e2b_api_key=os.getenv('E2B_API_KEY', ''),
                        notion_enabled=connectors_config.get("notion_mcp", {}).get("enabled", False),
                        notion_api_token=os.getenv('NOTION_API_TOKEN', ''),
                        fileboss_enabled=connectors_config.get("fileboss", {}).get("enabled", True),
                        fileboss_root_path=connectors_config.get("fileboss", {}).get("root_path", "./data/fileboss"),
                        parallel_execution=mcp_config_data.get("connector_settings", {}).get("parallel_execution", True),
                        max_workers=mcp_config_data.get("connector_settings", {}).get("max_workers", 4),
                        timeout_seconds=mcp_config_data.get("connector_settings", {}).get("timeout_seconds", 300)
                    )
                    
                    self.orchestrator = MCPOrchestrator(
                        config=config,
                        memory_bridge=self.memory_bridge
                    )
                
                # Initialize legal analyzer
                if LegalIntelligenceAnalyzer and self.memory_bridge:
                    self.legal_analyzer = LegalIntelligenceAnalyzer(
                        memory_bridge=self.memory_bridge,
                        case_number=mcp_config_data.get("case_number"),
                        jurisdiction=mcp_config_data.get("jurisdiction"),
                        court_level=mcp_config_data.get("court_level")
                    )
                
                logger.info("MCP configuration loaded successfully")
                
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
    
    def compose(self) -> ComposeResult:
        """Create the application layout."""
        yield Header("🎯 Omni Engine MCP - Maximum Control Point Intelligence")
        
        with Horizontal():
            # Control Panel
            with Vertical(id="control_panel"):
                yield Label("⚡ MCP Control Center", classes="header")
                yield Button("🚀 Execute Intelligence", id="execute_intelligence")
                yield Button("📊 Run Analysis", id="run_analysis")
                yield Button("🔄 Refresh Status", id="refresh_status")
                yield Button("💾 Export Report", id="export_report")
                yield Button("🧹 Clear Logs", id="clear_logs")
                yield Label("")
                yield Label("Connector Controls:", classes="header")
                yield Switch(value=True, id="fileboss_switch")
                yield Label("FILEBOSS")
                yield Switch(value=False, id="github_switch")
                yield Label("GitHub MCP")
                yield Switch(value=False, id="gdrive_switch")
                yield Label("Google Drive")
                yield Switch(value=False, id="e2b_switch")
                yield Label("E2B Sandbox")
                yield Switch(value=False, id="notion_switch")
                yield Label("Notion AI")
                
                yield ProgressBar(total=100, id="execution_progress")
                
            # Main Dashboard
            with Vertical(id="main_dashboard"):
                with TabbedContent():
                    with TabPane("🔌 MCP Status", id="status_tab"):
                        yield MCPStatusWidget(self.orchestrator)
                    
                    with TabPane("🧠 Intelligence", id="intelligence_tab"):
                        self.intelligence_widget = IntelligenceWidget()
                        yield self.intelligence_widget
                    
                    with TabPane("📝 Memory Bridge", id="memory_tab"):
                        yield RichLog(id="memory_log", auto_scroll=True)
                    
                    with TabPane("⚙️ System Logs", id="logs_tab"):
                        yield RichLog(id="system_log", auto_scroll=True)
        
        yield Static("🎯 GitHub MASTER - MCP Ready ⚡", id="status_bar")
        yield Footer()
    
    @on(Button.Pressed, "#execute_intelligence")
    def execute_intelligence_gathering(self) -> None:
        """Execute comprehensive intelligence gathering."""
        if not self.orchestrator:
            self.log_message("MCP Orchestrator not initialized", "error")
            return
        
        self.log_message("Starting intelligence gathering...", "info")
        
        # Run in background to avoid blocking UI
        asyncio.create_task(self._async_execute_intelligence())
    
    async def _async_execute_intelligence(self) -> None:
        """Asynchronously execute intelligence gathering."""
        try:
            progress = self.query_one("#execution_progress", ProgressBar)
            progress.update(progress=10)
            
            # Execute orchestrated intelligence gathering
            results = self.orchestrator.execute_orchestrated_intelligence_gathering()
            progress.update(progress=70)
            
            self.log_message(f"Intelligence gathering completed: {results.get('total_entries_generated', 0)} entries", "success")
            
            # Run legal analysis if analyzer available
            if self.legal_analyzer:
                analysis_results = self.legal_analyzer.perform_comprehensive_analysis()
                progress.update(progress=90)
                
                # Update intelligence widget
                if self.intelligence_widget:
                    self.intelligence_widget.intelligence_data = analysis_results
                
                self.log_message("Legal intelligence analysis completed", "success")
            
            progress.update(progress=100)
            
        except Exception as e:
            self.log_message(f"Intelligence execution failed: {e}", "error")
            logger.error(f"Intelligence execution error: {e}")
    
    @on(Button.Pressed, "#run_analysis")
    def run_legal_analysis(self) -> None:
        """Run legal intelligence analysis."""
        if not self.legal_analyzer:
            self.log_message("Legal analyzer not initialized", "error")
            return
        
        try:
            self.log_message("Running legal intelligence analysis...", "info")
            results = self.legal_analyzer.perform_comprehensive_analysis()
            
            if self.intelligence_widget:
                self.intelligence_widget.intelligence_data = results
            
            self.log_message("Legal analysis completed successfully", "success")
            
        except Exception as e:
            self.log_message(f"Legal analysis failed: {e}", "error")
    
    @on(Button.Pressed, "#refresh_status")
    def refresh_status(self) -> None:
        """Refresh MCP status display."""
        status_widget = self.query_one(MCPStatusWidget)
        status_widget.update_status()
        self.log_message("Status refreshed", "info")
    
    @on(Button.Pressed, "#export_report")
    def export_report(self) -> None:
        """Export comprehensive intelligence report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = Path(f"./reports/omni_intelligence_report_{timestamp}.json")
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            if self.legal_analyzer and self.legal_analyzer.analysis_results:
                self.legal_analyzer.export_analysis_report(report_path)
                self.log_message(f"Report exported: {report_path}", "success")
            else:
                self.log_message("No analysis results to export", "warn")
                
        except Exception as e:
            self.log_message(f"Export failed: {e}", "error")
    
    @on(Button.Pressed, "#clear_logs")
    def clear_logs(self) -> None:
        """Clear all log displays."""
        for log_id in ["#memory_log", "#system_log"]:
            try:
                log = self.query_one(log_id, RichLog)
                log.clear()
            except:
                pass
        self.log_message("Logs cleared", "info")
    
    def log_message(self, message: str, level: str = "info") -> None:
        """Log message to system log."""
        try:
            log = self.query_one("#system_log", RichLog)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            color_map = {
                "info": "cyan",
                "success": "green", 
                "warn": "yellow",
                "error": "red"
            }
            
            color = color_map.get(level, "white")
            log.write(f"[{color}][{timestamp}][/] {message}")
            
        except Exception as e:
            logger.error(f"Failed to log message: {e}")


def run_mcp_gui(config_path: str = "mcp_config.json") -> None:
    """Run the MCP-enhanced Omni Engine GUI."""
    import os
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('omni_engine_mcp.log'),
            logging.StreamHandler()
        ]
    )
    
    app = OmniEngineMCPApp(config_path)
    app.run()


if __name__ == "__main__":
    import sys
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else "mcp_config.json"
    run_mcp_gui(config_file)
