#!/usr/bin/env python3
"""Reference Fiedler spectral bipartition for EST8717 lab 6.

L = D − A. Second eigenvector (Fiedler) via shifted inverse iteration.
Sort nodes, sweep balanced prefixes, pick minimum cutsize.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


Edge = tuple[str, str, float]


def load_graph(path: Path) -> tuple[list[str], list[Edge], dict[str, float]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    nodes = [str(n) for n in doc["nodes"]]
    edges: list[Edge] = []
    for e in doc["edges"]:
        u, v, w = str(e["u"]), str(e["v"]), float(e["w"])
        if u == v:
            continue
        edges.append((u, v, w))
    sizes = {n: float(doc.get("node_sizes", {}).get(n, 1.0)) for n in nodes}
    return nodes, edges, sizes


def cutsize(assignment: dict[str, str], edges: list[Edge]) -> float:
    total = 0.0
    for u, v, w in edges:
        if assignment[u] != assignment[v]:
            total += w
    return total


def parts_string(assignment: dict[str, str]) -> str:
    groups: dict[str, list[str]] = {}
    for n, c in assignment.items():
        groups.setdefault(c, []).append(n)
    labs = ["".join(sorted(members)) for members in groups.values()]
    return "|".join(sorted(labs))


def _laplacian(nodes: list[str], edges: list[Edge]) -> list[list[float]]:
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    L = [[0.0] * n for _ in range(n)]
    for u, v, w in edges:
        i, j = idx[u], idx[v]
        L[i][j] -= w
        L[j][i] -= w
        L[i][i] += w
        L[j][j] += w
    return L


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: list[float]) -> float:
    return math.sqrt(_dot(a, a))


def spectral_bisection(
    nodes: list[str],
    edges: list[Edge],
    sizes: dict[str, float] | None = None,
) -> tuple[dict[str, str], list[tuple[str, float]]]:
    """Fiedler bisection via shifted inverse iteration (pure Python, tiny n)."""
    n = len(nodes)
    if n < 2:
        return {nodes[0]: "0"}, [(nodes[0], 0.0)]
    L = _laplacian(nodes, edges)
    ones = [1.0 / math.sqrt(n)] * n
    x = [1.0 if i % 2 == 0 else -1.0 for i in range(n)]
    x = [xi - _dot(x, ones) * ones[i] for i, xi in enumerate(x)]
    xn = _norm(x) or 1.0
    x = [xi / xn for xi in x]

    eps = 1e-3
    M = [row[:] for row in L]
    for i in range(n):
        M[i][i] += eps

    for _ in range(80):
        y = x[:]
        for _sweep in range(40):
            y_new = y[:]
            for i in range(n):
                s = x[i] - sum(M[i][j] * y[j] for j in range(n) if j != i)
                y_new[i] = s / M[i][i]
            y = y_new
        y = [yi - _dot(y, ones) * ones[i] for i, yi in enumerate(y)]
        yn = _norm(y) or 1.0
        x = [yi / yn for yi in y]

    order = sorted(zip(nodes, x), key=lambda t: (t[1], t[0]))
    sizes = sizes or {name: 1.0 for name in nodes}
    total = sum(sizes[name] for name in nodes)
    best_asn: dict[str, str] | None = None
    best_cut = float("inf")
    for k in range(1, n):
        left = {order[i][0] for i in range(k)}
        asn = {name: ("0" if name in left else "1") for name in nodes}
        frac = sum(sizes[name] for name in left) / total
        if frac < 0.2 or frac > 0.8:
            continue
        c = cutsize(asn, edges)
        if c < best_cut - 1e-12:
            best_cut = c
            best_asn = asn
    if best_asn is None:
        k = n // 2
        left = {order[i][0] for i in range(k)}
        best_asn = {name: ("0" if name in left else "1") for name in nodes}
    return best_asn, order


def main() -> None:
    ap = argparse.ArgumentParser(description="Spectral bipartition (Fiedler prefix sweep)")
    ap.add_argument("graph", type=Path, help="JSON graph with nodes and edges")
    args = ap.parse_args()
    nodes, edges, sizes = load_graph(args.graph)
    asn, order = spectral_bisection(nodes, edges, sizes)
    n0 = sum(1 for n in nodes if asn[n] == "0")
    n1 = sum(1 for n in nodes if asn[n] == "1")
    print(f"parts={parts_string(asn)}  cutsize={int(cutsize(asn, edges))}  balance={n0} vs {n1}")
    print("order=" + " ".join(n for n, _ in order))
    for name, val in order:
        print(f"  Fiedler {name}: {val:.4f}")


if __name__ == "__main__":
    main()
