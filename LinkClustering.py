import sys
import pandas as pd

def calc_linkage(edges_list, adj_matrix):
	num_nodes = len(adj_matrix)
	link_adj_matrix = [[0 for _ in range(len(edges_list))] for _ in range(len(edges_list))]

	edges_dict = {}
	for i, edge in enumerate(edges_list):
		edges_dict[tuple(edge)] = i
		edges_dict[tuple(reversed(edge))] = i

	for i in range(num_nodes):
		for j in range(num_nodes):			
			for k in range(num_nodes):
				if adj_matrix[i][k] > 0 and adj_matrix[j][k] > 0:
					i_neighbors = []				
					for ei_index, ei in enumerate(adj_matrix[i]):
						if ei > 0:
							i_neighbors.append(ei_index)
					j_neighbors = []
					for ej_index, ej in enumerate(adj_matrix[j]):
						if ej > 0:
							j_neighbors.append(ej_index)

					shared_neighbors = len(set(i_neighbors).intersection(j_neighbors))
					total_neighbors = len(set(i_neighbors).union(j_neighbors))					
			
					link_adj_matrix[edges_dict[(i, k)]][edges_dict[(j, k)]] = float(shared_neighbors) / float(total_neighbors)

	return link_adj_matrix


def cluster_link(link_adj_matrix, num_clusters=2):
	clusters = [[i] for i in range(len(link_adj_matrix))]

	while len(clusters) > num_clusters:		
		max_cluster = 0
		max_cluster_other = 0
		max_cluster_dist = 0

		for i in range(len(clusters)):
			for j in range(i + 1, len(clusters)):					
					
					# Calculate dist between two clusters
					cur_dist = 0
					for ei in clusters[i]:
						for ej in clusters[j]:
							if link_adj_matrix[ei][ej] > cur_dist:
								cur_dist = link_adj_matrix[ei][ej]

					if cur_dist > max_cluster_dist:
						max_cluster = i
						max_cluster_other = j
						max_cluster_dist = cur_dist

		clusters[max_cluster] = clusters[max_cluster] + clusters[max_cluster_other]
		del clusters[max_cluster_other]

	return clusters

def cluster(nodes_list, edges_list, adj_matrix, num_clusters=2):
	link_clusters = cluster_link(calc_linkage(edges_list, adj_matrix), num_clusters=num_clusters)
	node_clusters = []

	for cluster in link_clusters:
		cur_node_cluster = set()
		for e in cluster:
			cur_node_cluster.add(nodes_list[edges_list[e][0]][0])
			cur_node_cluster.add(nodes_list[edges_list[e][1]][0])
		node_clusters.append(list(cur_node_cluster))

	return node_clusters

num_clusters = 7

nodes_data = pd.read_csv("nodeslist.csv", engine="python", sep=",")
nodes_list = nodes_data[["id"]].values.tolist()

num_nodes = len(nodes_list)
nodes = {}
for i, node in enumerate(nodes_list):
	nodes[node[0]] = i

edges_data = pd.read_csv("stormofswords.csv", engine="python", sep=",")
edges_list = edges_data[["Source", "Target"]].values.tolist()
edges_list = map(lambda e: [nodes[e[0]], nodes[e[1]]], edges_list)

adj_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
for e in edges_list:
	adj_matrix[e[0]][e[1]] = 1
	adj_matrix[e[1]][e[0]] = 1

print cluster(nodes_list, edges_list, adj_matrix, num_clusters=num_clusters)
