import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, box, LineString, Point
import numpy as np


# 生成六边形格栅
def generate_hex_grid(rect, hex_size):
    minx, miny, maxx, maxy = rect.bounds
    dx = 3 / 2 * hex_size
    dy = np.sqrt(3) * hex_size

    hexagons = []
    for x in np.arange(minx - hex_size, maxx + hex_size, dx):
        for y in np.arange(miny - hex_size, maxy + hex_size, dy):
            if int(x / dx) % 2 == 0:
                y_offset = y
            else:
                y_offset = y + dy / 2

            hexagon = Polygon([
                (x + hex_size * np.cos(np.radians(angle)), y_offset + hex_size * np.sin(np.radians(angle)))
                for angle in range(0, 360, 60)
            ])
            intersection = rect.intersection(hexagon)
            if intersection.is_valid:
                hexagons.append(intersection)

    return hexagons


# 检查并分割矩形边
def check_and_split_rect_edges(rect, hexagons):
    rect_edges = [LineString([rect.exterior.coords[i], rect.exterior.coords[i + 1]]) for i in
                  range(len(rect.exterior.coords) - 1)]
    split_edges = []

    for edge in rect_edges:
        split_points = []
        for hexagon in hexagons:
            if isinstance(hexagon, Polygon):  # 确保 hexagon 是 Polygon 对象
                for point in hexagon.exterior.coords:
                    point_obj = Point(point)
                    if edge.intersects(point_obj):
                        split_points.append(point_obj)

        # 如果找到分割点，则按分割点分割边
        if split_points:
            split_points = sorted(set(split_points), key=lambda p: edge.project(p))
            split_segments = []
            prev_point = Point(edge.coords[0])
            for p in split_points:
                segment = LineString([prev_point, p])
                split_segments.append(segment)
                prev_point = p
            segment = LineString([prev_point, Point(edge.coords[1])])
            split_segments.append(segment)
            split_edges.extend(split_segments)
        else:
            split_edges.append(edge)

    return split_edges


# 删除重复边，包含方向相反的边
def remove_duplicate_edges(edges, tolerance=1e-2):
    filtered_edges = []
    seen_edges = set()

    for edge in edges:
        start, end = edge.coords[0], edge.coords[-1]
        # 将起点和终点都四舍五入到小数点后两位
        start = (round(start[0], 2), round(start[1], 2))
        end = (round(end[0], 2), round(end[1], 2))

        # 确保 start 总是比 end 小，以便处理方向相反但实际相同的边
        if start > end:
            start, end = end, start
        edge_tuple = (start, end)

        # 检查该边（标准形式）是否之前出现过
        if edge_tuple not in seen_edges:
            seen_edges.add(edge_tuple)
            filtered_edges.append(LineString([start, end]))

    return filtered_edges


# 处理并输出边
def process_and_output_edges(hexagons, rect):
    edges = []

    # 分割并添加矩形的边
    rect_edges = check_and_split_rect_edges(rect, hexagons)
    for edge in rect_edges:
        formatted_coords = [(round(x, 2), round(y, 2)) for x, y in edge.coords]
        if len(formatted_coords) == 2 and formatted_coords[0] != formatted_coords[1]:
            edges.append(LineString(formatted_coords))

    # 处理六边形的边
    for hexagon in hexagons:
        if isinstance(hexagon, Polygon):  # 确保 hexagon 是 Polygon 对象
            for i in range(len(hexagon.exterior.coords) - 1):
                edge = LineString([hexagon.exterior.coords[i], hexagon.exterior.coords[i + 1]])
                if edge.length > 0:
                    formatted_coords = [(round(x, 2), round(y, 2)) for x, y in edge.coords]
                    if len(formatted_coords) == 2 and formatted_coords[0] != formatted_coords[1]:
                        edges.append(LineString(formatted_coords))

    # 删除起点和终点相同的边，并移除方向相反的边
    edges = remove_duplicate_edges(edges)
    return edges


# 绘制矩形和六边形格栅
def plot_hex_grid(edges, rect):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Polygon(list(rect.exterior.coords), fill=None, edgecolor='blue'))

    for edge in edges:
        x, y = zip(*edge.coords)
        ax.plot(x, y, color='black')

    ax.set_aspect('equal')
    plt.show()


# 定义矩形范围
rect = box(0, 0, 100, 100)

# 生成六边形格栅并处理边
hex_size = 2 # 六边形的大小
hexagons = generate_hex_grid(rect, hex_size)
edges = process_and_output_edges(hexagons, rect)

# 输出最终保留的边
print("Final edges:")
for edge in edges:
    print(list(edge.coords))

# 可视化结果
plot_hex_grid(edges, rect)
