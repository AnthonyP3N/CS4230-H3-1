# CS 4230 - Assignment H3-1, Problem 1
# Degree, closeness and betweenness centrality of the Twitter network.
#
# Run:  python problem1.py
# (twitter_combined.txt must be in the same folder)
 
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
 
random.seed(42)
 
# The graph has ~81K nodes, which is too big to compute closeness and
# betweenness exactly for every node in a reasonable time (~50 hours).
# So we use samples:
#   - betweenness: NetworkX's built-in estimate from K random source nodes
#   - closeness:   exact closeness for a random sample of nodes (for the
#                  histogram) plus the top-200 degree nodes (for part 1.3)
BETWEENNESS_K = 500
CLOSENESS_SAMPLE = 1000
TOP_N = 200
 
# Problem 1.1
# Read the directed network
twitter = nx.read_edgelist('twitter_combined.txt',
                           create_using=nx.DiGraph(), nodetype=int)
print("Directed graph:   nodes =", twitter.order(), " edges =", twitter.size())
 
# Convert to an undirected network (and drop self-loops)
twitter_ud = twitter.to_undirected()
twitter_ud.remove_edges_from(nx.selfloop_edges(twitter_ud))
print("Undirected graph: nodes =", twitter_ud.order(), " edges =", twitter_ud.size())
 
# Keep the largest connected component
print("Connected components:", nx.number_connected_components(twitter_ud))
largest = max(nx.connected_components(twitter_ud), key=len)
G = twitter_ud.subgraph(largest).copy()
print("Largest component: nodes =", G.order(), " edges =", G.size())
 
# Degree centrality (exact)
deg_cen = nx.degree_centrality(G)
 
# Top-200 nodes by degree centrality (needed for 1.3)
top_nodes = sorted(deg_cen, key=deg_cen.get, reverse=True)[:TOP_N]
 
# Betweenness centrality (estimated from BETWEENNESS_K random source nodes)
print("Computing betweenness centrality (about 15 min)...")
bet_cen = nx.betweenness_centrality(G, k=BETWEENNESS_K, seed=42)
 
# Closeness centrality (exact, for a random sample + the top-200 nodes)
print("Computing closeness centrality (about 10 min)...")
sample_nodes = random.sample(list(G.nodes()), CLOSENESS_SAMPLE)
clo_cen = {}
for node in sample_nodes + top_nodes:
    clo_cen[node] = nx.closeness_centrality(G, u=node)


# Problem 1.2
def save_histogram(values, title, xlabel, filename):
    plt.figure()
    plt.hist(values, bins=50)
    plt.yscale('log')          # log scale so the long tail is visible
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Number of nodes (log scale)')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    print("Saved", filename)
 
save_histogram(list(deg_cen.values()),
               'Degree centrality (all %d nodes)' % G.order(),
               'Degree centrality', 'hist_degree.png')
save_histogram([clo_cen[n] for n in sample_nodes],
               'Closeness centrality (%d random nodes)' % CLOSENESS_SAMPLE,
               'Closeness centrality', 'hist_closeness.png')
save_histogram(list(bet_cen.values()),
               'Betweenness centrality (all %d nodes)' % G.order(),
               'Betweenness centrality', 'hist_betweenness.png')
 
# Problem 1.3
def print_stats(label, values):
    print("  %-28s mean = %.6g   median = %.6g   std = %.6g"
          % (label, np.mean(values), np.median(values), np.std(values)))
 
print("\nTop %d nodes by degree centrality:" % TOP_N)
print_stats("closeness centrality", [clo_cen[n] for n in top_nodes])
print_stats("betweenness centrality", [bet_cen[n] for n in top_nodes])
 
# The same statistics for the whole network, for comparison
print("\nAll nodes (for comparison):")
print_stats("degree centrality", list(deg_cen.values()))
print_stats("closeness (random sample)", [clo_cen[n] for n in sample_nodes])
print_stats("betweenness centrality", list(bet_cen.values()))
 

