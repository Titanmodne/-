import numpy as np
import trimesh
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


def sample_points_from_stl(file_path, interval):
    # Load the STL file using trimesh
    mesh = trimesh.load(file_path)

    # Get the bounding box of the mesh
    bounding_box = mesh.bounds
    min_bounds, max_bounds = bounding_box[0], bounding_box[1]

    # Generate points within the bounding box at the specified interval
    x_points = np.arange(min_bounds[0], max_bounds[0], interval)
    y_points = np.arange(min_bounds[1], max_bounds[1], interval)
    z_points = np.arange(min_bounds[2], max_bounds[2], interval)

    # Create a meshgrid of points
    grid = np.meshgrid(x_points, y_points, z_points)
    points = np.vstack([np.ravel(axis) for axis in grid]).T

    # Check which points are inside the mesh
    inside_points = []
    for point in points:
        if mesh.contains([point]):
            inside_points.append(point)

    return np.array(inside_points)


def main():
    # Create a GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select an STL file
    file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])

    if file_path:
        # Ask the user to input the interval distance
        interval = simpledialog.askfloat("Input", "Enter the interval distance in millimeters:", minvalue=0.1)

        if interval is not None:
            points = sample_points_from_stl(file_path, interval)
            print(f"Sampled {len(points)} points from the STL file.")

            # Save points to a file if needed
            np.savetxt('sampled_points.txt', points, delimiter=',')
            print("Points saved to sampled_points.txt")


if __name__ == "__main__":
    main()
