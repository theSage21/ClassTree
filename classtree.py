import os
import ast
import sys
from graphviz import Digraph
from pathlib import Path

vertices, edges = set(), set()


class ClassVisitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        vertices.add(node.name)
        for base in node.bases:
            if hasattr(base, "name"):
                parent = base.name
            elif hasattr(base, "id"):
                parent = base.id
            else:
                parent = str(base)
            edges.add((parent, node.name))


root = Path(sys.argv[1])
for r, d, f in os.walk(root):
    for file in f:
        file = root / r / file
        if os.path.isfile(file):
            if not str(file).endswith(".py"):
                continue
            with open(file, "r") as fl:
                code = fl.read()
            tree = ast.parse(code)
            ClassVisitor().visit(tree)

dot = Digraph(comment="Class Hierarchy", format="svg")

for v in vertices:
    dot.node(v)

for a, b in edges:
    dot.edge(a, b)
dot.view()
dot.save()
