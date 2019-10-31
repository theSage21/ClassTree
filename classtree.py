import os
import ast
import sys
from graphviz import Digraph

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


for file in os.listdir(sys.argv[1]):
    file = os.path.join(sys.argv[1], file)
    if not file.endswith(".py"):
        continue
    with open(file, "r") as fl:
        code = fl.read()
    tree = ast.parse(code)
    ClassVisitor().visit(tree)

dot = Digraph(comment="Class Hierarchy")

for v in vertices:
    dot.node(v, v)

for a, b in edges:
    dot.edge(a, b)
dot.view()
