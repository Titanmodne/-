import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point


class EdgePrinter:
    import numpy as np
    import matplotlib.pyplot as plt
    from shapely.geometry import LineString, Point

    class EdgePrinter:
        def __init__(self, width, height, hex_size, precision=2):
            self.width = width
            self.height = height
            self.hex_size = hex_size
            self.precision = precision  # Precision for rounding
            self.precision_threshold = 0.02  # Precision threshold for merging points
            self.hexagons = self.generate_hex_grid()
            self.rectangle_edges = self.get_rectangle_edges()
            self.hexagon_edges = self.get_hexagon_edges()
            self.split_rectangle_edges = self.split_edges_by_intersections()
            self.sorted_edges = self.sort_edges(self.split_rectangle_edges)

        def generate_hex_grid(self):
            num_hex_x = int(self.width // (3 / 2 * self.hex_size))
            num_hex_y = int(self.height // (np.sqrt(3) * self.hex_size))

            hexagons = []

            for i in range(num_hex_x + 1):
                for j in range(num_hex_y + 1):
                    x = round(i * 3 / 2 * self.hex_size, 2)
                    y = round(j * np.sqrt(3) * self.hex_size, 2)

                    if i % 2 == 1:
                        y = round(y + np.sqrt(3) / 2 * self.hex_size, 2)  # Offset every other row

                    hexagon = self.create_hexagon(x, y, self.hex_size)
                    hexagons.append(hexagon)

            return hexagons

        def create_hexagon(self, x_center, y_center, size):
            angles = np.linspace(0, 2 * np.pi, 7)
            x_hex = np.round(x_center + size * np.cos(angles), 2)
            y_hex = np.round(y_center + size * np.sin(angles), 2)
            return list(zip(x_hex, y_hex))

        def get_rectangle_edges(self):
            vertices = [
                (0, 0, 0),
                (self.width, 0, 0),
                (self.width, self.height, 0),
                (0, self.height, 0)
            ]

            edges = []
            for i in range(len(vertices)):
                start_vertex = vertices[i]
                end_vertex = vertices[(i + 1) % len(vertices)]
                edges.append((self.normalize_point(start_vertex), self.normalize_point(end_vertex)))

            return edges

        def get_hexagon_edges(self):
            edges = set()
            for hexagon in self.hexagons:
                for i in range(len(hexagon) - 1):
                    edge = tuple(sorted((self.normalize_point((hexagon[i][0], hexagon[i][1], 0)),
                                         self.normalize_point((hexagon[i + 1][0], hexagon[i + 1][1], 0)))))
                    edges.add(edge)
            return list(edges)

        def split_edges_by_intersections(self):
            new_edges = set()
            for rect_edge in self.rectangle_edges:
                rect_line = LineString([rect_edge[0][:2], rect_edge[1][:2]])
                intersections = []

                for hex_edge in self.hexagon_edges:
                    hex_line = LineString([hex_edge[0][:2], hex_edge[1][:2]])
                    if rect_line.intersects(hex_line):
                        intersection = rect_line.intersection(hex_line)
                        if isinstance(intersection, Point):
                            intersections.append(
                                self.normalize_point((round(intersection.x, 2), round(intersection.y, 2), 0)))
                        elif isinstance(intersection, LineString):
                            intersections.extend([self.normalize_point((round(pt[0], 2), round(pt[1], 2), 0)) for pt in
                                                  intersection.coords])

                # Normalize and sort intersections
                intersections = sorted(set(self.normalize_point(p) for p in intersections),
                                       key=lambda p: np.hypot(p[0] - rect_edge[0][0], p[1] - rect_edge[0][1]))
                split_points = [rect_edge[0]] + intersections + [rect_edge[1]]

                for i in range(len(split_points) - 1):
                    p1 = self.normalize_point(split_points[i])
                    p2 = self.normalize_point(split_points[i + 1])
                    if not self.is_same_point(p1, p2, tolerance=self.precision_threshold):
                        edge = tuple(sorted((p1, p2)))
                        new_edges.add(edge)

            return list(new_edges)

        def is_same_point(self, point1, point2, tolerance=0.02):
            return (
                    abs(point1[0] - point2[0]) < tolerance and
                    abs(point1[1] - point2[1]) < tolerance and
                    abs(point1[2] - point2[2]) < tolerance
            )

        def normalize_point(self, point):
            return (
                round(point[0], self.precision),
                round(point[1], self.precision),
                round(point[2], self.precision)
            )

        def sort_edges(self, edges):
            def sort_key(edge):
                p1, p2 = edge
                return (p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])

            return sorted(edges, key=sort_key)

        def print_edges(self):
            print("Sorted Rectangle Edges:")
            for edge in self.sorted_edges:
                print(f"{edge[0]}, {edge[1]}")

            print("\nHexagon Edges:")
            for edge in self.hexagon_edges:
                print(f"{edge[0]}, {edge[1]}")

        def plot_edges(self):
            plt.figure(figsize=(10, 10))

            for edge in self.sorted_edges:
                x_values = [edge[0][0], edge[1][0]]
                y_values = [edge[0][1], edge[1][1]]
                plt.plot(x_values, y_values, 'r-')

            for hexagon in self.hexagons:
                hex_x, hex_y = zip(*hexagon)
                plt.plot(hex_x, hex_y, 'b-')

            plt.xlim(0, self.width)
            plt.ylim(0, self.height)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()

    # Example usage
    if __name__ == "__main__":
        # Parameters
        width = 20  # Width of the rectangle
        height = 15  # Height of the rectangle
        hex_size = 1  # Size of each hexagon

        edge_printer = EdgePrinter(width, height, hex_size)
        edge_printer.print_edges()  # Print the sorted rectangle edges and hexagon edges
        edge_printer.plot_edges()  # Plot the edges (optional)


# Example usage
if __name__ == "__main__":
    # Parameters
    width = 20  # Width of the rectangle
    height = 15  # Height of the rectangle
    hex_size = 1  # Size of each hexagon

    edge_printer = EdgePrinter(width, height, hex_size)
    edge_printer.print_edges()  # Print the split rectangle edges and hexagon edges
    edge_printer.plot_edges()  # Plot the edges (optional)
