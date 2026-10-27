# Lab 06 — Spectral bipartition

Local browser lab for **learn_partitioning** module `module02-05-spectral-partition` (Lab 06 of 13). Same five-node netlist as greedy pair merge / KL / FM.

Spectral bipartition is a **global initializer**:

1. Build the graph Laplacian \(L = D - A\).
2. Take the **Fiedler vector** (second eigenvector of \(L\)).
3. Sort nodes low → high.
4. Sweep **balanced prefixes** and pick minimum cutsize.
5. Report **parts, cutsize, and balance**.

Live course pages:

- [Spectral bipartition lab](https://yongfu-li.github.io/eda-learning/courses/learn_partitioning/labs/spectral-partition/index.html)
- [spectral-partition tool](https://yongfu-li.github.io/eda-learning/tools/spectral-partition/index.html)
- [Module on GitHub](https://github.com/SJTU-YONGFU-RESEARCH-GRP/eda-learning/tree/main/courses/learn_partitioning/module02-05-spectral-partition)

## Run the page

Serve this folder (needed for video and relative assets):

```bash
cd partitioning_l6
python3 -m http.server 8766 --bind 0.0.0.0
```

Open [http://127.0.0.1:8766/index.html](http://127.0.0.1:8766/index.html).

English / 中文 is a header toggle. The page uses `i18n.js`. Locked terms:

| English | 中文 |
| --- | --- |
| Graph Laplacian | 图拉普拉斯矩阵 |
| Eigenvector / Eigenvalue | 特征向量 / 特征值 |
| Similarity graph | 相似度图 |
| Normalized Cut (Ncut) | 归一化割 |
| RatioCut | 比率割 |
| Spectrum | 谱 |

## What is on the page

Three tabs, modeled on the clustering lab:

| Tab | Contents |
| --- | --- |
| **Lab** | Language clip, steps, interactive graph (run / step Fiedler sweep, join remaining cut), checklist, quiz |
| **Game** | Match-the-terms plus short missions |
| **Course notes** | Slide walkthrough, implement track, pitfalls |

**Videos** (under `media/`):

- English: `media/spectral-en.mp4` — visual hook plus course walkthrough (Your turn at ~1:55)
- 中文: `media/spectral-zh.mp4`

Narration script: [`transcript.md`](transcript.md). Session plan: [`lesson_plan.md`](lesson_plan.md).

Optional slides (CDN): PPTX / PDF links on the lab toolbar.

## Starter graph (`tiny_graph`)

[`examples/tiny_graph.json`](examples/tiny_graph.json) — undirected weighted graph. Parallel edges sum; self-loops ignored.

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

Balance filter on this instance: prefix fraction in **[0.2, 0.8]**.

### Fiedler order (low → high)

**E, D, C, B, A** (E most negative, A most positive).

### Winning prefix

`{D,E}` vs `{A,B,C}` — cut edges C–D (2) and C–E (1) — **cutsize 3**. Heavy trunks A–B and D–E stay inside.

Golden line:

```text
parts=ABC|DE  cutsize=3  balance=2 vs 3
order=E D C B A
```

(`DE|ABC` is the same communities with sides swapped.)

## Browser track

1. Load the starter graph.
2. **Run spectral**. Confirm order starts at **E** and ends at **A**.
3. Confirm parts `ABC|DE`, cutsize **3**, balance **2 vs 3**.
4. Join the remaining cut on the graph (click two nodes, same interaction as Lab 03).
5. Work challenges: cutsize 3, two labels, D with E, C with A/B.

## Implement track

Reference solver: [`common/solvers.py`](common/solvers.py) (pure Python Fiedler via shifted inverse iteration).

```bash
python3 common/solvers.py examples/tiny_graph.json
```

Expected:

```text
parts=ABC|DE  cutsize=3  balance=2 vs 3
order=E D C B A
```

Re-implement Laplacian, Fiedler (or a tiny eigensolver), sort, balanced prefix sweep, then print assignment + cutsize + balance.

## Quiz

Six recall items on the Lab tab, all from Course notes / `transcript.md` (not outside logic puzzles):

1. Primary algorithm: spectral bipartition (Laplacian / Fiedler), not greedy / KL / FM.
2. Laplacian \(L = D - A\).
3. Fiedler vector = second eigenvector of \(L\).
4. Report parts, cutsize, and balance.
5. Order **E, D, C, B, A**.
6. Winning prefix **{D,E} vs {A,B,C}, cutsize 3**.

## Pitfalls (from the notes)

- Cutsize without balance is not the contract — report both.
- Fiedler sign can flip; sort and sweep; do not hard-code “negative = left.”
- A sign cut at 0 is **not** the same as a balanced prefix sweep (C is near zero).
- Spectral is an initializer. Later labs (KL / FM / multilevel) refine; they do not replace the Laplacian step here.

## Layout

```text
partitioning_l6/
  index.html              Lab / Game / Course notes / quiz
  i18n.js                 English + 中文 strings
  lesson_plan.md          90-minute session plan
  transcript.md           Course voiceover (~2:54)
  examples/tiny_graph.json
  common/solvers.py
  media/                  EN/ZH clips and TTS sources
```
