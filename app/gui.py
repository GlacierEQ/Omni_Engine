"""Interactive dashboard for the Omni Engine memory bridge."""

from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

from modules.operator import AuditReport, OperatorCore, build_default_operator


class MemoryBridgeApp(App):
    """Textual-based dashboard for monitoring connectors and layers."""

    CSS_PATH = Path(__file__).with_suffix(".css")
    BINDINGS = [
        Binding("r", "refresh", "Refresh", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self, operator: OperatorCore | None = None) -> None:
        super().__init__()
        self.operator = operator or build_default_operator()
        self.report: AuditReport | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(
            Vertical(
                Static("Connectors", id="connectors_title"),
                DataTable(id="connectors_table"),
                id="connectors_panel",
            ),
            Vertical(
                Static("Memory Layers", id="layers_title"),
                DataTable(id="layers_table"),
                id="layers_panel",
            ),
            Vertical(
                Static("Recommendations", id="recs_title"),
                Static(id="recs_body"),
                Button("Refresh", id="refresh_button"),
                id="recs_panel",
            ),
            id="dashboard",
        )
        yield Footer()

    def on_mount(self) -> None:
        connectors_table = self.query_one("#connectors_table", DataTable)
        connectors_table.add_columns("Connector", "Produced", "Layers", "Alerts")

        layers_table = self.query_one("#layers_table", DataTable)
        layers_table.add_columns("Layer", "Entries")

        self.call_after_refresh(self.refresh_data)

    def action_refresh(self) -> None:
        self.refresh_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh_button":
            self.refresh_data()

    def refresh_data(self) -> None:
        self.report = self.operator.run_cycle()
        self._populate_connectors()
        self._populate_layers()
        self._populate_recommendations()

    def _populate_connectors(self) -> None:
        table = self.query_one("#connectors_table", DataTable)
        table.clear()
        if not self.report:
            return
        for audit in self.report.connectors:
            layers_summary = ", ".join(f"{layer}:{count}" for layer, count in audit.layer_counts.items())
            alerts = str(len(audit.alerts)) if audit.alerts else "0"
            table.add_row(audit.name, str(audit.produced), layers_summary or "-", alerts)

    def _populate_layers(self) -> None:
        table = self.query_one("#layers_table", DataTable)
        table.clear()
        snapshot = self.operator.layer_snapshot()
        for layer, entries in snapshot.items():
            table.add_row(layer, str(len(entries)))

    def _populate_recommendations(self) -> None:
        body = self.query_one("#recs_body", Static)
        if not self.report:
            body.update("No data available.")
            return
        recommendations = self.operator.generate_recommendations(self.report)
        formatted = "\n".join(f"• {rec}" for rec in recommendations)
        body.update(formatted)


def run() -> None:
    """Launch the dashboard using the default operator configuration."""

    app = MemoryBridgeApp()
    app.run()


__all__ = ["MemoryBridgeApp", "run"]
