"""Generate a knowledge graph of internal module dependencies.

This script parses all Python files under the ``src`` directory and
creates a GraphViz ``.dot`` file representing import relationships
between modules in this project.

Usage::

    python src/tools/knowledge_graph.py

The output ``knowledge_graph.dot`` can be rendered using GraphViz::

    dot -Tpng knowledge_graph.dot -o graph.png
"""

from __future__ import annotations

import ast
import os
from pathlib import Path
from typing import Dict, Iterable, List


BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"


def iter_py_files(base: Path = SRC_DIR) -> Iterable[Path]:
    """Yield all Python files under ``base``."""
    for root, _, files in os.walk(base):
        for file in files:
            if file.endswith(".py"):
                yield Path(root) / file


def parse_imports(path: Path) -> List[str]:
    """Return a list of imported modules from ``path``."""
    with path.open("r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(path))
    modules: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module)
    return modules


def build_dependency_graph() -> Dict[str, List[str]]:
    """Build a mapping of module -> imported modules within ``src``."""
    graph: Dict[str, List[str]] = {}
    for py_file in iter_py_files():
        module = py_file.relative_to(SRC_DIR).with_suffix("").as_posix().replace("/", ".")
        imports = []
        for name in parse_imports(py_file):
            if name.startswith("src."):
                imports.append(name[4:])
        graph[module] = sorted(set(imports))
    return graph


def export_dot(graph: Dict[str, List[str]], output: Path) -> None:
    """Write ``graph`` to ``output`` in GraphViz DOT format."""
    lines = ["digraph G {"]
    for module, deps in sorted(graph.items()):
        for dep in deps:
            lines.append(f'    "{module}" -> "{dep}";')
    lines.append("}")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    graph = build_dependency_graph()
    export_dot(graph, BASE_DIR / "knowledge_graph.dot")
    print("Graph written to knowledge_graph.dot")


if __name__ == "__main__":
    main()
