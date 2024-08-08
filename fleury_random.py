import random
import networkx as nx
from collections import defaultdict
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Function to generate random 3D points
def generate_random_3d_points(num_points, precision=0.1):
    points = []
    for _ in range(num_points):
        x = round(random.uniform(0, 100), 1)
        y = round(random.uniform(0, 100), 1)
        z = round(random.uniform(0, 0), 1)
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


# Function to apply offset along the normal of the edges
def apply_offset_along_normal(edges, offset=2):
    offset_edges = []
    for edge in edges:
        p1, p2 = edge
        direction = np.array(p2) - np.array(p1)
        direction = direction / np.linalg.norm(direction)  # Normalize direction

        # Compute a vector perpendicular to the edge direction
        normal = np.cross(direction, [0, 0, 1])
        if np.linalg.norm(normal) == 0:  # If the edge is parallel to z-axis, use another direction
            normal = np.cross(direction, [1, 0, 0])
        normal = normal / np.linalg.norm(normal)  # Normalize normal vector

        p1_offset = tuple(np.array(p1) + offset * normal)
        p2_offset = tuple(np.array(p2) + offset * normal)
        offset_edges.append((p1_offset, p2_offset))
    return offset_edges


# Function to calculate the distance between two points
def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


# Function to find the minimum cost combination of copied edges
def find_minimum_cost_combination(edges, copied_edges):
    min_cost = float('inf')
    best_combination = None

    for combination in combinations(copied_edges, 4):  # Assuming we want combinations of 4 edges
        cost = 0
        for edge in combination:
            p1, p2 = edge
            cost += distance(p1, p2)
        if cost < min_cost:
            min_cost = cost
            best_combination = combination

    return best_combination, min_cost


# Function to plot the Eulerian path with replaced and offset edges
def plot_eulerian_path_with_replacement(path_edges, copied_edges, offset_edges, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Unpack points into separate lists
    x, y, z = zip(*points)
    ax.scatter(x, y, z, c='r', marker='o')

    # Draw the original path edges in blue
    for edge in path_edges:
        if edge not in copied_edges and edge not in offset_edges:
            p1, p2 = edge
            x_vals = [p1[0], p2[0]]
            y_vals = [p1[1], p2[1]]
            z_vals = [p1[2], p2[2]]
            ax.plot(x_vals, y_vals, z_vals, 'b-',
                    label='Original Path' if 'Original Path' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Draw the copied edges in green
    for edge in copied_edges:
        p1, p2 = edge
        x_vals = [p1[0], p2[0]]
        y_vals = [p1[1], p2[1]]
        z_vals = [p1[2], p2[2]]
        ax.plot(x_vals, y_vals, z_vals, 'g--',
                label='Copied Edge' if 'Copied Edge' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Draw the offset edges in orange
    for edge in offset_edges:
        p1, p2 = edge
        x_vals = [p1[0], p2[0]]
        y_vals = [p1[1], p2[1]]
        z_vals = [p1[2], p2[2]]
        ax.plot(x_vals, y_vals, z_vals, 'orange', linestyle=':',
                label='Offset Edge' if 'Offset Edge' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Eulerian Path with Replaced and Offset Edges')
    plt.legend()
    plt.show()


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

    offset_copied_edges = apply_offset_along_normal(copied_edges)

    print("\nOffset Copied Edges:")
    for edge in offset_copied_edges:
        print(edge)

    best_combination, min_cost = find_minimum_cost_combination(offset_copied_edges, copied_edges)

    print("\nBest Combination of Copied Edges:")
    for edge in best_combination:
        print(edge)

    print(f"\nMinimum Total Cost: {min_cost}")

    # Plot the Eulerian Path with replaced and offset edges
    plot_eulerian_path_with_replacement(euler_path, best_combination, offset_copied_edges, points)


# Run the main function
if __name__ == "__main__":
    main()
