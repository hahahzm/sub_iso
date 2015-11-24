# sub_iso
Zero-Knowledge Interactive Protocol for Subgraph Isomorphism

Python server and client communicating throuth network socket

Input: Adjacency matrices
Output: Accept/Reject

To run server:
	python prover.py [PORT] [Directory of graph]


To run client:
	python verifier.py [HOST] [PORT] [Directory of graph]

Each directory of a graph contains 6 files: 
	G1: graph g1
	G2: graph g2
	G': the secret subgraph only known by server
	G1-G': the isomorphism between G1 and G', only known by server, too

G' has the same dimension as G2 in terms of adjacency matrix. Vertices that are not in G' are marked with weight of 2. Normal edges are of weight 1, not-connected are of weight 0. 


G1-G' contains integer pairs like
a b
c d
...

which means vertex a in graph G1 corresponds to vertex b in graph G'

*One example of such graph set is included. 

