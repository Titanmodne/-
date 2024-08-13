from collections import defaultdict


# 构建图，使用邻接表表示
def build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# 检查图中所有节点的度数
def get_degrees(graph):
    degrees = defaultdict(int)
    for u in graph:
        degrees[u] = len(graph[u])
    return degrees


# 找到奇数度数的节点
def find_odd_vertices(degrees):
    return [v for v, degree in degrees.items() if degree % 2 == 1]


# 检查图是否连通
def is_connected(graph):
    if not graph:
        return True

    visited = set()
    start_node = next(iter(graph))

    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)
    return len(visited) == len(graph)


# 使用 Fleury 算法生成欧拉回路或路径
def fleury_algorithm(graph, start):
    graph = {u: list(vs) for u, vs in graph.items()}  # 复制图，避免修改原图
    path = []

    def is_bridge(u, v):
        # 暂时移除边(u, v)和(v, u)来检查是否是桥
        graph[u].remove(v)
        graph[v].remove(u)
        is_conn = is_connected(graph)
        graph[u].append(v)
        graph[v].append(u)
        return not is_conn

    def find_eulerian_path(u):
        stack = [u]
        path = []
        while stack:
            u = stack[-1]
            if graph[u]:
                v = graph[u][0]
                if is_bridge(u, v) and len(graph[u]) > 1:
                    # 找到非桥的边来避免无效路径
                    for neighbor in graph[u]:
                        if neighbor != v:
                            v = neighbor
                            break
                path.append((u, v))
                graph[u].remove(v)
                graph[v].remove(u)
                stack.append(v)
            else:
                stack.pop()
                if stack:
                    path.append((stack[-1], u))
        return path

    return find_eulerian_path(start)


def main(edges):
    graph = build_graph(edges)
    degrees = get_degrees(graph)
    odd_vertices = find_odd_vertices(degrees)

    if not is_connected(graph):
        raise ValueError("图的一个或多个节点的度数为0，无法生成欧拉路径或回路")

    start = next(iter(graph))
    if len(odd_vertices) == 2:
        start = odd_vertices[0]

    eulerian_path = fleury_algorithm(graph, start)

    # 处理并去除重复的反向边
    seen_edges = set()
    path_with_reverse = []
    for u, v in eulerian_path:
        if (u, v) not in seen_edges and (v, u) not in seen_edges:
            path_with_reverse.append((u, v))
            seen_edges.add((u, v))
            seen_edges.add((v, u))  # 添加反向边

    return path_with_reverse


# 输入边列表
edges = [
    ((10.0, 0.0), (10.0, 4.79)),
    ((10.0, 4.79), (10.0, 8.0)),
    ((7.85, 8.0), (10.0, 8.0)),
    ((4.15, 8.0), (7.85, 8.0)),
    ((0.0, 8.0), (4.15, 8.0)),
    ((0.0, 4.79), (0.0, 8.0)),
    ((0.0, 0.0), (0.0, 4.79)),
    ((0.0, 0.0), (3.23, 0.0)),
    ((3.23, 0.0), (8.77, 0.0)),
    ((8.77, 0.0), (10.0, 0.0)),
    ((0.0, 4.79), (3.0, 4.79)),
    ((3.0, 4.79), (4.5, 2.2)),
    ((3.23, 0.0), (4.5, 2.2)),
    ((4.15, 8.0), (4.5, 7.39)),
    ((3.0, 4.79), (4.5, 7.39)),
    ((4.5, 2.2), (7.5, 2.2)),
    ((7.5, 2.2), (8.77, 0.0)),
    ((4.5, 7.39), (7.5, 7.39)),
    ((7.5, 7.39), (9.0, 4.79)),
    ((7.5, 2.2), (9.0, 4.79)),
    ((7.5, 7.39), (7.85, 8.0)),
    ((9.0, 4.79), (10.0, 4.79)),
]

# 生成欧拉路径或回路
eulerian_path = main(edges)
for u, v in eulerian_path:
    print(f'{u} -> {v}')
