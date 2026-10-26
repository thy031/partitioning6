# Lab 6 plan — spectral bipartition

**Module:** `learn_partitioning` · 05 spectral partition (`module02-05-spectral-partition`)  
**Live lab:** [Spectral bipartition](https://yongfu-li.github.io/eda-learning/courses/learn_partitioning/labs/spectral-partition/index.html)  
**Live tool:** [spectral-partition](https://yongfu-li.github.io/eda-learning/tools/spectral-partition/index.html)  
**Starter graph:** [`examples/tiny_graph.json`](examples/tiny_graph.json)  
**Reference solver:** [`common/solvers.py`](common/solvers.py)  
**Local page:** [`index.html`](index.html)

Local copy of Lab 06 of 13. Same five-node netlist as greedy pair merge / KL / FM. Spectral reads the Laplacian, sorts the Fiedler vector, then sweeps **balanced prefixes** for the cheapest cut.

---

## 1. Why this engine

Spectral bipartition is a **global initializer**, not a greedy merge:

- Laplacian \(L = D - A\) encodes connectivity.
- The **Fiedler vector** (second eigenvector of \(L\)) is a soft 1-D embedding.
- Sort nodes low→high, then try every **balanced** prefix as side 0.
- Pick the prefix with **minimum cutsize**. Report **parts, cutsize, and balance**.

On `tiny_graph` the winning split is the same golden communities as unconstrained greedy: `ABC|DE` (or `DE|ABC`) with **cutsize 3**.

---

## 2. Key content

### 2.1 Input

Undirected weighted graph. Parallel edges sum. Self-loops ignored.

| Edge | Weight |
| --- | ---: |
| A–B | 5 |
| B–C | 4 |
| C–D | 2 |
| D–E | 5 |
| A–C | 1 |
| C–E | 1 |
| **All separate cutsize** | **18** |

Degrees: A=6, B=9, C=8, D=7, E=6.

### 2.2 Ranking / cut rule

```text
INPUT: weighted undirected G
OUTPUT: side[] bipartition
L ← Laplacian; take Fiedler eigenvector
order ← nodes sorted by Fiedler value
sweep balanced prefixes; pick min cutsize
GOLDEN: DE|ABC (or ABC|DE) cut=3
```

Balance filter on this tiny instance: prefix fraction in **[0.2, 0.8]** (reject 1-vs-4 lopsided cuts if they fall outside).

### 2.3 Fiedler order (shifted inverse iteration)

Low → high: **E, D, C, B, A**.

Approximate values (unit Fiedler vector, orthogonal to all-ones):

| Node | Fiedler |
| --- | ---: |
| E | −0.5533 |
| D | −0.4889 |
| C | +0.1057 |
| B | +0.4176 |
| A | +0.5190 |

E is most negative; A is most positive.

### 2.4 Prefix sweep

| Prefix (side 0) | Complement | Cut edges | Cutsize |
| --- | --- | --- | ---: |
| E | ABCD | D–E (5), C–E (1) | 6 |
| **DE** | **ABC** | **C–D (2), C–E (1)** | **3** |
| CDE | AB | A–C (1), B–C (4) | 5 |
| BCDE | A | A–B (5), A–C (1) | 6 |

Winner: `{D,E}` vs `{A,B,C}`. Remaining cut is the weak bridges. Heavy trunks A–B and D–E stay **inside**.

### 2.5 Pitfalls

- Cutsize **without balance** is not the contract — report both.
- Sign of the Fiedler vector can flip; sort and sweep, do not hard-code “negative = left.”
- Zero-threshold (sign cut) is **not** the same as a balanced prefix sweep; C is near zero.
- Spectral is an initializer. Later labs (KL / FM / multilevel) refine; they do not replace the Laplacian step here.

---

## 3. Session flow (90 min)

| Min | Block | What happens |
| ---: | --- | --- |
| 0–10 | Hook | \(L = D - A\); Fiedler = second eigenvector. |
| 10–30 | Walkthrough | Order E–D–C–B–A. Predict the winning prefix **before** revealing cut 3. |
| 30–55 | Browser track | Load starter, **Run spectral**, work challenges (cut 3, ABC\|DE, E lowest, A highest). |
| 55–80 | Implement track | Match `parts=ABC\|DE  cutsize=3`. |
| 80–90 | Checklist + quiz | Exit ticket. |

---

## 4. Browser lab track

1. Load the `tiny_graph` starter.
2. Click **Run spectral**. Confirm Fiedler order starts at **E** and ends at **A**.
3. Confirm parts `ABC|DE`, cutsize **3**, balance **2 vs 3** (side 0 = DE, side 1 = ABC).
4. Work challenges: cutsize 3, two labels, D and E together, C with A/B, bridge cut with reveal off.

---

## 5. Implement track

```bash
python3 common/solvers.py examples/tiny_graph.json
```

Expected:

```text
parts=ABC|DE  cutsize=3  balance=2 vs 3
order=E D C B A
```

Re-implement: Laplacian, Fiedler (or call a tiny eigensolver), sort, balanced prefix sweep, print assignment + cutsize + balance.

---

## 6. Quiz (from Course notes + `transcript.md`)

All six items are recall from the notes, not outside logic puzzles.

1. Primary algorithm: **spectral bipartition (graph Laplacian / Fiedler vector)** — not greedy / KL / FM.
2. Graph Laplacian: **L = D − A**.
3. Fiedler vector: **second eigenvector of L** (not the all-ones / λ=0 vector).
4. Report **part assignment plus cutsize and balance**.
5. Fiedler order low→high: **E, D, C, B, A**.
6. Winning balanced prefix: **{D,E} vs {A,B,C}, cutsize 3**.
