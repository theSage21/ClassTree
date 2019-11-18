import os
from itertools import cycle
import ast
from collections import defaultdict
import sys
from graphviz import Digraph, ENGINES
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "paths", metavar="N", type=str, nargs="+",
)
parser.add_argument("--list-orphans", default=False, action="store_true")
parser.add_argument(
    "--engine", default="dot", choices=ENGINES, action="store", type=str
)
args = parser.parse_args()
vertices, edges = set(), set()
detail_map = defaultdict(dict)


class ClassVisitor(ast.NodeVisitor):
    def __init__(self, src_path):
        self.src_path = src_path
        super().__init__()

    def visit_ClassDef(self, node):
        vertices.add(node.name)
        detail_map[node.name]["lineno"] = node.lineno
        detail_map[node.name]["src_path"] = self.src_path
        for base in node.bases:
            if hasattr(base, "name"):
                parent = base.name
            elif hasattr(base, "id"):
                parent = base.id
            else:
                parent = str(base)
            edges.add((parent, node.name))


for path in args.paths:
    root = Path(path)
    for r, d, f in os.walk(root):
        for file in f:
            file = root / r / file
            if os.path.isfile(file):
                if not str(file).endswith(".py"):
                    continue
                with open(file, "r") as fl:
                    code = fl.read()
                tree = ast.parse(code)
                ClassVisitor(file).visit(tree)

if args.list_orphans:
    for vert in vertices:
        if not any(vert in edge for edge in edges):
            print(vert)
else:
    unique_files = list(
        sorted(set(detail.get("src_path") for detail in detail_map.values()))
    )
    colormap = dict(
        zip(
            map(str, unique_files),
            cycle(
                [
                    "Black",
                    "Yellow",
                    "Blue",
                    "Red",
                    "Green",
                    "Brown",
                    "Azure",
                    "Ivory",
                    "Purple",
                    "Orange",
                    "Maroon",
                    "Aquamarine",
                    "Coral",
                    "Fuchsia",
                    "Wheat",
                    "Lime",
                    "Crimson",
                    "Khaki",
                    "Hot pink",
                    "Magenta",
                    "Plum",
                    "Olive",
                    "Cyan",
                ]
            ),
        )
    )

    dot = Digraph(name="ClassTree", format="svg", engine=args.engine)
    for k, v in colormap.items():
        dot.node(k, color=v)
    for v in vertices:
        color = colormap[str(detail_map[v]["src_path"])]
        dot.node(v, color=color)

    for a, b in edges:
        dot.edge(a, b)
    dot.view()
