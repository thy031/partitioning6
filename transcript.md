This is the narration from the Lab 06 clip (~2:54). It is the course’s own voiceover script, timed from the slide audio.

0:00 — Title
Spectral bipartition reads connectivity from the graph Laplacian. The Fiedler vector gives a soft ordering of nodes; a balanced sweep of that order picks the cut. On the starter graph the winning split is DE versus ABC with cutsize three.

0:16 — The idea
Build L equals D minus A, take the second eigenvector, sort nodes, and try balanced prefixes. Reject lopsided splits. The continuous membership becomes a hard bipartition only after the sweep chooses the best legal cut.

0:32 — Pseudocode
Spectral bipartition reads the Fiedler vector of the Laplacian, sorts nodes, then sweeps balanced prefixes for the cheapest cut.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

0:50 — Algorithm sketch
On the starter graph the winning split is D E versus A B C with cutsize three—the same golden communities KL and FM refine toward.

0:53 — Code slide (no voiceover)
The screen shows:


INPUT: weighted undirected G
OUTPUT: side[] bipartition
L ← Laplacian; take Fiedler eigenvector
order ← nodes sorted by Fiedler value
sweep balanced prefixes; pick min cutsize
GOLDEN: DE|ABC (or ABC|DE) cut=3
0:58 — Build the Laplacian
Spectral methods read connectivity from the graph Laplacian L = D − A. The Fiedler vector (second eigenvector) encodes a soft cut.

1:09 — Sort by Fiedler value
After iteration, nodes order low→high as E, D, C, B, A. E is most negative; A is most positive — natural bipartition candidates.

1:19 — Sweep prefixes for best cut
Try every balanced prefix of the order as side 0. The winning split is {D,E} vs {A,B,C} with cutsize 3.

1:29 — Result ABC|DE
Spectral recovers the same communities as unconstrained greedy and grow-from-D. Global eigenvectors find the cut without greedy merges.

1:37 — When spectral helps
Spectral is a strong initializer for bipartition. On larger chips it pairs with multilevel; here the tiny instance grades against golden cut 3.

1:47 — Browser lab track
In the browser lab track, open the spectral-partition lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

2:04 — Implement track
In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

2:22 — Pitfalls
Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

2:40 — Your turn
Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.