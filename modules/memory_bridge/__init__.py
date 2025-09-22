"""Public interface for the memory bridge package."""

from .bridge import MemoryBridge
from .catalog import FunctionSpec, McpCatalog
from .entry import MemoryEntry
from .fusion import FusionLoop
from .layer import MemoryLayer
from .node import IntelligenceNode
from .witness import WitnessNetwork

__all__ = [
    "MemoryBridge",
    "FunctionSpec",
    "McpCatalog",
    "MemoryEntry",
    "MemoryLayer",
    "IntelligenceNode",
    "WitnessNetwork",
    "FusionLoop",
]
