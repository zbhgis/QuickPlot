"""
custom_marker() can add custom marker style

Author: https://github.com/zbhgis
Last Modified: 2025-07-30
"""

import matplotlib.path as mpath
import numpy as np


def custom_marker(marker_type="n+"):
    """
    生成自定义标记路径（支持 n+, nx, n*, oo, ox, sx 四种类型）

    参数:
        marker_type (str): 标记类型，可选 "n+", "nx", "n*", "oo", "ox", "sx"

    返回:
        matplotlib.path.Path: 对应的标记路径
    """
    if marker_type == "r":
        # 双圆环（外圆半径1，内圆半径0.5）
        theta = np.linspace(0, 2 * np.pi, 100)
        outer_x, outer_y = np.cos(theta), np.sin(theta)
        inner_x, inner_y = 0.5 * np.cos(theta), 0.5 * np.sin(theta)
        # 组合内外圆路径（用MOVETO/LINETO连接）
        vertices = np.vstack(
            [
                np.column_stack([outer_x, outer_y]),
                np.column_stack([inner_x[::-1], inner_y[::-1]]),  # 内圆反向绘制
            ]
        )
        codes = (
            [mpath.Path.LINETO] * len(outer_x)
            + [mpath.Path.MOVETO]
            + [mpath.Path.LINETO] * len(inner_x)
        )
        codes[0] = mpath.Path.MOVETO  # 第一个点设为MOVETO
        return mpath.Path(vertices, codes)

    elif marker_type == "ox":
        # 圆内x（外圆+对角线）
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x, circle_y = np.cos(theta), np.sin(theta)
        # x的对角线（缩放至圆内）
        x_lines = [[-0.7, -0.7], [0.7, 0.7], [-0.7, 0.7], [0.7, -0.7]]
        # 组合路径
        vertices = np.vstack([np.column_stack([circle_x, circle_y]), x_lines])
        codes = [mpath.Path.LINETO] * len(circle_x) + [
            mpath.Path.MOVETO,
            mpath.Path.LINETO,
        ] * 2
        codes[0] = mpath.Path.MOVETO
        return mpath.Path(vertices, codes)

    elif marker_type == "sx":
        # 方内x（正方形+对角线）
        square = [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]  # 闭合正方形
        x_lines = [[-0.7, -0.7], [0.7, 0.7], [-0.7, 0.7], [0.7, -0.7]]
        vertices = np.vstack([square, x_lines])
        codes = (
            [mpath.Path.MOVETO]
            + [mpath.Path.LINETO] * 4
            + [mpath.Path.MOVETO, mpath.Path.LINETO] * 2
        )
        return mpath.Path(vertices, codes)

    else:
        # 定义基础线段（单位长度1）
        if marker_type == "n+":
            # + 加号（水平和垂直线）
            segments = [
                [[-1, 0], [1, 0]],  # 水平线
                [[0, -1], [0, 1]],  # 垂直线
            ]
        elif marker_type == "nx":
            # x 乘号（两条对角线）
            segments = [
                [[-0.7, -0.7], [0.7, 0.7]],  # 主对角线
                [[-0.7, 0.7], [0.7, -0.7]],  # 副对角线
            ]
        elif marker_type == "n*":
            # * 星号（+ 和 x 的组合）
            segments = [
                [[-1, 0], [1, 0]],  # 水平线
                [[0, -1], [0, 1]],  # 垂直线
                [[-0.7, -0.7], [0.7, 0.7]],  # 主对角线
                [[-0.7, 0.7], [0.7, -0.7]],  # 副对角线
            ]
        else:
            raise ValueError(f"不支持的类型: {marker_type}。")

        # 将线段转换为Path需要的格式
        vertices = []
        codes = []
        for seg in segments:
            vertices.extend(seg)
            codes.extend([mpath.Path.MOVETO, mpath.Path.LINETO])  # 每条线段独立绘制

        return mpath.Path(np.array(vertices), codes)
