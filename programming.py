import collections
import re
import tkinter as tk
from tkinter import filedialog


# 从txt文件读取边信息并生成图
def read_graph_from_file(file_path):
    graph = collections.defaultdict(list)
    edges = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            matches = re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', content)
            for match in matches:
                u, v = map(int, match)
                if u != v:  # 避免自环
                    if u < v:
                        edge = (u, v)
                    else:
                        edge = (v, u)
                    if edge not in edges:
                        graph[u].append(v)
                        graph[v].append(u)
                        edges.add(edge)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
    return graph, edges


# Fleury算法实现
def is_valid_next_edge(graph, u, v):
    # 如果u节点只有一个边，说明这条边是必要的
    if len(graph[u]) == 1:
        return True

    # 检查图是否连通
    visited = set()
    count1 = dfs_count(graph, u, visited)

    # 临时移除边
    graph[u].remove(v)
    graph[v].remove(u)

    visited.clear()
    count2 = dfs_count(graph, u, visited)

    # 添加边回来
    graph[u].append(v)
    graph[v].append(u)

    return count1 == count2


def dfs_count(graph, u, visited):
    visited.add(u)
    count = 1
    for v in graph[u]:
        if v not in visited:
            count += dfs_count(graph, v, visited)
    return count


def fleury_algorithm(graph, start):
    path = []

    def visit(u):
        for v in list(graph[u]):
            if is_valid_next_edge(graph, u, v):
                path.append((u, v))
                # Debugging statement
                print(f"Traversing edge ({u}, {v})")

                # 移除边
                graph[u].remove(v)
                graph[v].remove(u)

                visit(v)
                return

    visit(start)
    return path


# 文件选择器模块
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


# 从txt文件读取图
file_path = select_file()
graph, edges = read_graph_from_file(file_path)
print("Graph Edges from File:", edges)

# 查找起始节点，选择一个度数为奇数的节点作为起始节点
odd_degree_nodes = [node for node in graph if len(graph[node]) % 2 == 1]
start_node = odd_degree_nodes[0] if odd_degree_nodes else next(iter(graph))

# 运行Fleury算法
euler_path = fleury_algorithm(graph, start_node)
print("Euler Path:", euler_path)


# 验证路径覆盖了所有边且仅访问一次
def validate_euler_path(edges, path):
    edge_count = collections.Counter((min(u, v), max(u, v)) for u, v in path)
    original_edges = collections.Counter((min(u, v), max(u, v)) for u, v in edges)
    print("Edge Count from Path:", edge_count)
    print("Original Edges:", original_edges)
    return edge_count == original_edges


print("Is valid Euler Path:", validate_euler_path(edges, euler_path))
