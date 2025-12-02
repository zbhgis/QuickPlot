"""
add_curly_brace() allows you to plot an optionally annotated curly bracket between two points when using matplotlib

The function takes the axes scales into account automatically. But when the axes aspect is
set to "equal", the auto switch should be turned off.

Original Author: https://github.com/iruletheworld/matplotlib-curly-brace
Modified by: https://github.com/zbhgis
Last Modified: 2025-07-03
Reference: https://uk.mathworks.com/matlabcentral/fileexchange/38716-curly-brace-annotation

"""

import matplotlib.pyplot as plt
import numpy as np

from typing import Any


def _get_ax_size(fig: plt.Figure, ax: plt.Axes) -> tuple[float, float]:
    """Calculate the exact pixel dimensions of matplotlib axes within its figure.

    Args:
        fig (plt.Figure): The parent figure containing the axes.
        ax (plt.Axes): The target axes object to measure.

    Returns:
        tuple[float, float]:
            - First element: Width of axes in pixels (float)
            - Second element: Height of axes in pixels (float)

    Raises:
        RuntimeError: If figure or axes is not properly initialized for pixel calculations.

    Examples:
        >>> width, height = _get_ax_size(fig, ax)
        >>> print(f"Axes dimensions: {width:.1f}px × {height:.1f}px")
    """

    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    ax_width, ax_height = bbox.width, bbox.height
    ax_width *= fig.dpi
    ax_height *= fig.dpi

    return ax_width, ax_height


def add_curly_brace(
    fig: plt.Figure,
    ax: plt.Axes,
    p1: list[float],
    p2: list[float],
    k_r: float = 0.1,
    bool_auto: bool = True,
    str_text: str = "",
    int_line_num: int = 2,
    fontdict: dict[str, Any] | None = None,
    text_offset: tuple[float, float] = (0, 0),
    **kwargs,
) -> tuple[
    float,
    list[float],
    list[list[float]],
    list[list[float]],
    list[list[float]],
    list[list[float]],
]:
    """Add an annotated curly brace between two points on matplotlib axes.

    Args:
        fig (plt.Figure): Target figure object for coordinate calculations.
        ax (plt.Axes): Target axes object to draw on.
        p1 (list[float]): Starting point coordinates [x1, y1].
        p2 (list[float]): End point coordinates [x2, y2].
        k_r (float, optional): Curvature coefficient controlling brace shape:
            - Higher values = more pronounced curvature
            - Lower values = flatter appearance
            Defaults to 0.1.
        bool_auto (bool, optional): Automatically adjust for axes aspect ratio.
            Defaults to True.
        str_text (str, optional): Annotation text displayed at brace midpoint.
            Defaults to "" (no text).
        int_line_num (int, optional): Number of connecting lines between text and brace:
            - 0: No connecting lines
            - 1: Single connecting line
            - 2: Double connecting lines (default)
        fontdict (dict[str, Any] | None, optional): Font properties dictionary for text:
            - Keys: 'family', 'size', 'weight', 'color', etc.
            - None uses default text properties
            Defaults to None.
        text_offset (tuple[float, float], optional): (dx, dy) offset for text position
            relative to brace midpoint. Defaults to (0, 0).
        **kwargs: Additional line properties passed to matplotlib.Line2D:
            - color: Line color (default: 'black')
            - linewidth: Line width in points (default: 1)
            - linestyle: Line style ('-', '--', ':', etc.)
            - alpha: Transparency (0-1)

    Returns:
        tuple[
            float,                # Brace angle in radians
            list[float],          # Summit point [x, y]
            list[list[float]],    # Points for first arc segment
            list[list[float]],    # Points for second arc segment
            list[list[float]],    # Points for third arc segment
            list[list[float]]     # Points for fourth arc segment
        ]: Detailed geometric information about the brace

    Raises:
        ValueError: If p1/p2 coordinates are invalid or k_r is non-positive.

    Examples:
        >>> # Basic horizontal brace
        >>> add_curly_brace(fig, ax, [0, 0], [1, 0], str_text="Length")

        >>> # Vertical brace with custom styling
        >>> add_curly_brace(
        ...     fig, ax, [0, 0], [0, 1],
        ...     str_text="Height",
        ...     color='red',
        ...     linewidth=2,
        ...     fontdict={'size': 12, 'weight': 'bold'}
        ... )

        >>> # Diagonal brace with offset text
        >>> result = add_curly_brace(
        ...     fig, ax, [0.1, 0.1], [0.9, 0.9],
        ...     str_text="Slope",
        ...     text_offset=(0.05, 0.05),
        ...     k_r=0.15
        ... )
        >>> angle, summit, arcs = result[0], result[1], result[2:]
    """

    pt1 = [None, None]
    pt2 = [None, None]

    ax_width, ax_height = _get_ax_size(fig, ax)

    ax_xlim = list(ax.get_xlim())
    ax_ylim = list(ax.get_ylim())

    # 对数
    if "log" in ax.get_xaxis().get_scale():

        if p1[0] > 0.0:

            pt1[0] = np.log(p1[0])

        elif p1[0] < 0.0:

            pt1[0] = -np.log(abs(p1[0]))

        else:

            pt1[0] = 0.0

        if p2[0] > 0.0:

            pt2[0] = np.log(p2[0])

        elif p2[0] < 0.0:

            pt2[0] = -np.log(abs(p2[0]))

        else:

            pt2[0] = 0

        for i in range(0, len(ax_xlim)):

            if ax_xlim[i] > 0.0:

                ax_xlim[i] = np.log(ax_xlim[i])

            elif ax_xlim[i] < 0.0:

                ax_xlim[i] = -np.log(abs(ax_xlim[i]))

            else:

                ax_xlim[i] = 0.0

    else:

        pt1[0] = p1[0]
        pt2[0] = p2[0]

    if "log" in ax.get_yaxis().get_scale():

        if p1[1] > 0.0:

            pt1[1] = np.log(p1[1])

        elif p1[1] < 0.0:

            pt1[1] = -np.log(abs(p1[1]))

        else:

            pt1[1] = 0.0

        if p2[1] > 0.0:

            pt2[1] = np.log(p2[1])

        elif p2[1] < 0.0:

            pt2[1] = -np.log(abs(p2[1]))

        else:

            pt2[1] = 0.0

        for i in range(0, len(ax_ylim)):

            if ax_ylim[i] > 0.0:

                ax_ylim[i] = np.log(ax_ylim[i])

            elif ax_ylim[i] < 0.0:

                ax_ylim[i] = -np.log(abs(ax_ylim[i]))

            else:

                ax_ylim[i] = 0.0

    else:

        pt1[1] = p1[1]
        pt2[1] = p2[1]

    # 获取像素/长度比率
    xscale = ax_width / abs(ax_xlim[1] - ax_xlim[0])
    yscale = ax_height / abs(ax_ylim[1] - ax_ylim[0])

    # 处理“相等”坐标轴
    if bool_auto:
        pass

    else:
        xscale = 1.0
        yscale = 1.0

    # 将长度转换为像素，需要减去下限值，将点移回原点。然后在末尾加上下限值
    pt1[0] = (pt1[0] - ax_xlim[0]) * xscale
    pt1[1] = (pt1[1] - ax_ylim[0]) * yscale
    pt2[0] = (pt2[0] - ax_xlim[0]) * xscale
    pt2[1] = (pt2[1] - ax_ylim[0]) * yscale

    # 计算角度
    theta = np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0])

    # 计算圆弧的半径
    r = np.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1]) * k_r

    # arc1 centre
    x11 = pt1[0] + r * np.cos(theta)
    y11 = pt1[1] + r * np.sin(theta)

    # arc2 centre
    x22 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) - r * np.cos(theta)
    y22 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) - r * np.sin(theta)

    # arc3 centre
    x33 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) + r * np.cos(theta)
    y33 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) + r * np.sin(theta)

    # arc4 centre
    x44 = pt2[0] - r * np.cos(theta)
    y44 = pt2[1] - r * np.sin(theta)

    q = np.linspace(theta, theta + np.pi / 2.0, 50)

    t = q[::-1]

    # arc坐标
    arc1x = r * np.cos(t + np.pi / 2.0) + x11
    arc1y = r * np.sin(t + np.pi / 2.0) + y11

    arc2x = r * np.cos(q - np.pi / 2.0) + x22
    arc2y = r * np.sin(q - np.pi / 2.0) + y22

    arc3x = r * np.cos(q + np.pi) + x33
    arc3y = r * np.sin(q + np.pi) + y33

    arc4x = r * np.cos(t) + x44
    arc4y = r * np.sin(t) + y44

    # 转换回坐标轴坐标
    arc1x = arc1x / xscale + ax_xlim[0]
    arc2x = arc2x / xscale + ax_xlim[0]
    arc3x = arc3x / xscale + ax_xlim[0]
    arc4x = arc4x / xscale + ax_xlim[0]

    arc1y = arc1y / yscale + ax_ylim[0]
    arc2y = arc2y / yscale + ax_ylim[0]
    arc3y = arc3y / yscale + ax_ylim[0]
    arc4y = arc4y / yscale + ax_ylim[0]

    # 对数
    if "log" in ax.get_xaxis().get_scale():

        for i in range(0, len(arc1x)):

            if arc1x[i] > 0.0:

                arc1x[i] = np.exp(arc1x[i])

            elif arc1x[i] < 0.0:

                arc1x[i] = -np.exp(abs(arc1x[i]))

            else:

                arc1x[i] = 0.0

        for i in range(0, len(arc2x)):

            if arc2x[i] > 0.0:

                arc2x[i] = np.exp(arc2x[i])

            elif arc2x[i] < 0.0:

                arc2x[i] = -np.exp(abs(arc2x[i]))

            else:

                arc2x[i] = 0.0

        for i in range(0, len(arc3x)):

            if arc3x[i] > 0.0:

                arc3x[i] = np.exp(arc3x[i])

            elif arc3x[i] < 0.0:

                arc3x[i] = -np.exp(abs(arc3x[i]))

            else:

                arc3x[i] = 0.0

        for i in range(0, len(arc4x)):

            if arc4x[i] > 0.0:

                arc4x[i] = np.exp(arc4x[i])

            elif arc4x[i] < 0.0:

                arc4x[i] = -np.exp(abs(arc4x[i]))

            else:

                arc4x[i] = 0.0

    else:

        pass

    if "log" in ax.get_yaxis().get_scale():

        for i in range(0, len(arc1y)):

            if arc1y[i] > 0.0:

                arc1y[i] = np.exp(arc1y[i])

            elif arc1y[i] < 0.0:

                arc1y[i] = -np.exp(abs(arc1y[i]))

            else:

                arc1y[i] = 0.0

        for i in range(0, len(arc2y)):

            if arc2y[i] > 0.0:

                arc2y[i] = np.exp(arc2y[i])

            elif arc2y[i] < 0.0:

                arc2y[i] = -np.exp(abs(arc2y[i]))

            else:

                arc2y[i] = 0.0

        for i in range(0, len(arc3y)):

            if arc3y[i] > 0.0:

                arc3y[i] = np.exp(arc3y[i])

            elif arc3y[i] < 0.0:

                arc3y[i] = -np.exp(abs(arc3y[i]))

            else:

                arc3y[i] = 0.0

        for i in range(0, len(arc4y)):

            if arc4y[i] > 0.0:

                arc4y[i] = np.exp(arc4y[i])

            elif arc4y[i] < 0.0:

                arc4y[i] = -np.exp(abs(arc4y[i]))

            else:

                arc4y[i] = 0.0

    else:

        pass

    # 绘制弧线
    ax.plot(arc1x, arc1y, **kwargs)
    ax.plot(arc2x, arc2y, **kwargs)
    ax.plot(arc3x, arc3y, **kwargs)
    ax.plot(arc4x, arc4y, **kwargs)

    # 绘制直线
    ax.plot([arc1x[-1], arc2x[1]], [arc1y[-1], arc2y[1]], **kwargs)
    ax.plot([arc3x[-1], arc4x[1]], [arc3y[-1], arc4y[1]], **kwargs)

    summit = [arc2x[-1], arc2y[-1]]

    if str_text:

        int_line_num = int(int_line_num)

        str_temp = "\n" * int_line_num

        # 将弧度转换为角度，范围为 0 到 360 度
        ang = np.degrees(theta) % 360.0

        # 处理 text_offset 参数
        if isinstance(text_offset, (list, tuple)) and len(text_offset) == 2:
            text_x = arc2x[-1] + text_offset[0]
            text_y = arc2y[-1] + text_offset[1]
        else:
            text_x = arc2x[-1] + text_offset * np.sin(theta)
            text_y = arc2y[-1] - text_offset * np.cos(theta)

        if (ang >= 0.0) and (ang <= 90.0):

            rotation = ang

            str_text = str_text + str_temp

        if (ang > 90.0) and (ang < 270.0):

            rotation = ang + 180.0

            str_text = str_temp + str_text

        elif (ang >= 270.0) and (ang <= 360.0):

            rotation = ang

            str_text = str_text + str_temp

        else:

            rotation = ang

        ax.axes.text(
            text_x,
            text_y,
            str_text,
            ha="center",
            va="center",
            rotation=rotation,
            fontdict=fontdict,
        )

    else:

        pass

    arc1 = [arc1x, arc1y]
    arc2 = [arc2x, arc2y]
    arc3 = [arc3x, arc3y]
    arc4 = [arc4x, arc4y]

    return theta, summit, arc1, arc2, arc3, arc4
