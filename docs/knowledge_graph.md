# Knowledge Graph Generation

This guide explains how to generate a simple knowledge graph that shows
the relationships between modules inside DeerFlow.

1. Run the `knowledge_graph` script:

   ```bash
   python src/tools/knowledge_graph.py
   ```

   This will create a `knowledge_graph.dot` file in the repository root.

2. Render the graph using [GraphViz](https://graphviz.org/):

   ```bash
   dot -Tpng knowledge_graph.dot -o graph.png
   ```

   The generated image visualizes the internal import dependencies.

