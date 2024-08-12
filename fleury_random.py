import random
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


# Function to generate random 3D points
def generate_random_3d_points(num_points, precision=0.1):
    points = []
    for _ in range(num_points):
        x = round(random.uniform(0, 100), 1)
        y = round(random.uniform(0, 100), 1)
        z = round(random.uniform(0, 100), 1)
        points.append((x, y, z))
    return points


# Function to create edges from points
def create_edges_from_points(points):
    num_points = len(points)
    edges = []
    for i in range(num_points - 1):
        edges.append((points[i], points[i + 1]))
    edges.append((points[-1], points[0]))  # to make it circular
    return edges


# Function to add random edges to ensure graph is Eulerian
def make_eulerian(edges, points):
    G = nx.Graph()
    G.add_edges_from(edges)
    for i, point in enumerate(points):
        if G.degree(point) % 2 != 0:
            for j, other_point in enumerate(points):
                if i != j and G.degree(other_point) % 2 != 0 and not G.has_edge(point, other_point):
                    G.add_edge(point, other_point)
                    break
    return list(G.edges)


# Function to generate an Eulerian path
def generate_eulerian_path(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    is_eulerian = nx.is_eulerian(G)
    if not is_eulerian:
        print("Graph is not Eulerian, making it Eulerian...")
        edges = make_eulerian(edges, list(G.nodes))
    euler_path = list(nx.eulerian_circuit(G))
    return euler_path


# Function to apply offset to copied edges
def apply_offset(edges, offset=0.1):
    offset_edges = []
    for edge in edges:
        p1, p2 = edge
        p1_offset = (p1[0] + offset, p1[1] + offset, p1[2] + offset)
        p2_offset = (p2[0] + offset, p2[1] + offset, p2[2] + offset)
        offset_edges.append((p1_offset, p2_offset))
    return offset_edges


# Main function
def main():
    num_points = 20
    points = generate_random_3d_points(num_points)
    edges = create_edges_from_points(points)

    print("Generated Graph Edges:")
    for edge in edges:
        print(edge)

    euler_path = generate_eulerian_path(edges)

    print("\nEuler Path:")
    for edge in euler_path:
        print(edge)

    copied_edges = [euler_path[i] for i in random.sample(range(len(euler_path)), 4)]

    print("\nCopied Edges:")
    for edge in copied_edges:
        print(edge)

    offset_copied_edges = apply_offset(copied_edges)

    print("\nOffset Copied Edges:")
    for edge in offset_copied_edges:
        print(edge)


# Run the main function
if __name__ == "__main__":
    main()
