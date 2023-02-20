# ConcurrentCongestionControl
This repository is for my Winter 2022-2023 Directed Study on Nonlinear Programming.

The codebase saved here is a collection of files written for my final project: an analysis and optimization of TCP application-layer congestion and resource control, but also contains several implemented algorithms. 

Briefly, the files are
- maxminfairness.ipynb: a short, initial experiment with maxmin fairness in a toy case
- network.py: an implementation of a (Network, Link, Pipe) structure, with well-defined objects and an implementation of maxminfairness, the main model of the mapping from "# of TCP connections" to "throughput" that we use.
- shortest_path.py: by choosing to be agnostic to network structure, the problem of application-layer congestion control becomes simply optimization on the integer values in [n]^d, and this file tests how well a naive, locally-greedy strategy works for this problem
- simplex.py: This file contains an implementation of the simplex algorithm. The simplex algorithm solves general LP problems -- which consist of linear constraints and a linear objective -- which is useful since both (1) determining maximum total throughput and (2) determining maximum total resource usage are both LP problem.
