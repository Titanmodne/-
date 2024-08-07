import ezdxf
from gridpath import Line, Arc, Euler  # 替换 'your_module' 为你的模块名

# 读取 DXF 文件
doc = ezdxf.readfile('C:/Users/zhong/Desktop/1.dxf')

# 创建 Euler 对象
euler = Euler()

# 遍历所有 LINE 实体
for entity in doc.modelspace().query('LINE'):
    line = Line(e=entity)
    # 将 Line 对象添加到 Euler 对象的图中
    # 这里需要根据实际情况进行添加，比如添加到某个数据结构中
    # 假设 euler.graph 是一个二维列表，存储 Line 对象
    # 你可能需要根据具体情况调整代码
    # euler.graph.append([line])

# 遍历所有 ARC 实体
for entity in doc.modelspace().query('ARC'):
    arc = Arc(e=entity)
    # 将 Arc 对象添加到 Euler 对象的图中
    # 根据实际需要添加到数据结构中
    # euler.graph.append([arc])
