"""Generate a consolidated operational report using OperatorCore."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from modules.operator import OperatorCore


def main() -> None:
    operator = OperatorCore()
    context = (
        "Comprehensive review of custody, financial and medical aspects for"
        " upcoming hearings."
    )
    output_path = Path("docs/reports/system_recommendations.md")
    operator.export_report(output_path, context=context)
    print(f"Report written to {output_path}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
