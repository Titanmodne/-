from collections import defaultdict, deque


# 构建图的邻接表
def build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# 寻找度数为奇数的顶点
def find_odd_degree_vertices(graph):
    odd_vertices = []
    for vertex in graph:
        if len(graph[vertex]) % 2 != 0:
            odd_vertices.append(vertex)
    return odd_vertices


# 复制并反转边以使图满足欧拉路径的条件
def make_eulerian(graph, edges):
    odd_vertices = find_odd_degree_vertices(graph)
    while len(odd_vertices) > 0:
        v1 = odd_vertices.pop()
        v2 = odd_vertices.pop()
        graph[v1].append(v2)
        graph[v2].append(v1)
        edges.append((v1, v2))  # 复制并添加反转的边
    return graph


# 使用Fleury算法生成欧拉路径
def eulerian_path(graph):
    start_vertex = next(iter(graph))
    stack = [start_vertex]
    path = deque()

    while stack:
        vertex = stack[-1]
        if graph[vertex]:
            next_vertex = graph[vertex].pop()
            graph[next_vertex].remove(vertex)
            stack.append(next_vertex)
        else:
            path.appendleft(stack.pop())

    return list(path)


# 输入边列表
edges = [
    ((10.0, 0.0), (10.0, 4.79)),
    ((10.0, 4.79), (10.0, 8.0)),
    ((10.0, 8.0), (7.85, 8.0)),
    ((7.85, 8.0), (7.5, 7.39)),
    ((7.5, 7.39), (9.0, 4.79)),
    ((9.0, 4.79), (10.0, 4.79)),
    ((9.0, 4.79), (7.5, 2.2)),
    ((7.5, 2.2), (8.77, 0.0)),
    ((8.77, 0.0), (10.0, 0.0)),
    ((8.77, 0.0), (3.23, 0.0)),
    ((3.23, 0.0), (4.5, 2.2)),
    ((4.5, 2.2), (7.5, 2.2)),
    ((4.5, 2.2), (3.0, 4.79)),
    ((3.0, 4.79), (4.5, 7.39)),
    ((4.5, 7.39), (7.5, 7.39)),
    ((4.5, 7.39), (4.15, 8.0)),
    ((4.15, 8.0), (7.85, 8.0)),
    ((4.15, 8.0), (0.0, 8.0)),
    ((0.0, 8.0), (0.0, 4.79)),
    ((0.0, 4.79), (3.0, 4.79)),
    ((0.0, 4.79), (0.0, 0.0)),
    ((0.0, 0.0), (3.23, 0.0)),
]

# 构建图
graph = build_graph(edges)

# 调整图以满足欧拉路径条件
graph = make_eulerian(graph, edges)

# 生成欧拉路径
euler_path = eulerian_path(graph)

# 输出结果
if euler_path:
    print("欧拉路径为:")
    for i in range(len(euler_path) - 1):
        print(f"{euler_path[i]} -> {euler_path[i + 1]}")
else:
    print("不存在欧拉路径")
