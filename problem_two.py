# CS 4230 - Assignment H3-1, Problem 2
# Triadic census of the Twitter network (kept as a DIRECTED graph).
#
# Run:  python problem2.py
# (twitter_combined.txt must be in the same folder)
 
import networkx as nx
 
twitter = nx.read_edgelist('twitter_combined.txt',
                           create_using=nx.DiGraph(), nodetype=int)
twitter.remove_edges_from(nx.selfloop_edges(twitter))
print("Directed graph: nodes =", twitter.order(), " edges =", twitter.size())
 
# Counts of all 16 possible triad types (MAN codes: Mutual, Asymmetric, Null)
census = nx.triadic_census(twitter)
 
total = sum(census.values())
print("\n%-6s %18s %12s" % ("Triad", "Count", "Percent"))
for triad, count in census.items():
    print("%-6s %18d %11.4g%%" % (triad, count, 100.0 * count / total))
print("%-6s %18d" % ("Total", total))
 
# Sanity check: every set of 3 nodes is counted exactly once
n = twitter.order()
print("n choose 3 =", n * (n - 1) * (n - 2) // 6)