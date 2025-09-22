from __future__ import annotations

"""Catalog describing callable MCP functions."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class FunctionSpec:
    """Metadata describing a callable capability exposed to agents."""

    name: str
    description: str
    inputs: Mapping[str, str] = field(default_factory=dict)
    outputs: Mapping[str, str] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        name = self.name.strip()
        if not name:
            raise ValueError("Function name cannot be empty.")
        if not self.description.strip():
            raise ValueError("Function description cannot be empty.")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "inputs", MappingProxyType(dict(self.inputs)))
        object.__setattr__(self, "outputs", MappingProxyType(dict(self.outputs)))
        object.__setattr__(self, "tags", tuple(self.tags))

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the specification."""

        return {
            "name": self.name,
            "description": self.description,
            "inputs": dict(self.inputs),
            "outputs": dict(self.outputs),
            "tags": list(self.tags),
        }


class McpCatalog:
    """Registry of MCP callable descriptions."""

    def __init__(self) -> None:
        self._functions: dict[str, FunctionSpec] = {}

    def register(self, spec: FunctionSpec, *, replace: bool = False) -> None:
        """Register ``spec`` under its name.

        Parameters
        ----------
        spec:
            The function specification to add.
        replace:
            When ``True``, overwrite any existing entry with the same name.
        """

        if spec.name in self._functions and not replace:
            raise ValueError(f"Function '{spec.name}' is already registered.")
        self._functions[spec.name] = spec

    def remove(self, name: str) -> None:
        """Remove the specification identified by ``name``."""

        if name not in self._functions:
            raise KeyError(name)
        del self._functions[name]

    def get(self, name: str) -> FunctionSpec:
        """Return the registered specification with ``name``."""

        try:
            return self._functions[name]
        except KeyError as exc:  # pragma: no cover - defensive path
            raise KeyError(name) from exc

    def describe(self) -> list[dict[str, object]]:
        """Return all registered functions as dictionaries."""

        return [spec.to_dict() for spec in self._functions.values()]

    def clear(self) -> None:
        """Remove all registered functions."""

        self._functions.clear()

    def __contains__(self, name: str) -> bool:  # pragma: no cover - trivial
        return name in self._functions

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._functions)
