"""
add_line() can add custom lines in ax

Author: https://github.com/zbhgis
Last Modified: 2025-07-13
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def add_line(
    ax: plt.Axes,
    x: np.ndarray | list[float],
    y: np.ndarray | list[float],
    style: str = "-",
    linewidth: float = 1,
    color: str | None = "black",
    alpha: float = 1.0,
    zorder: int | None = None,
    transform: str | None = None,
    **kwargs,
) -> Line2D:
    """Add a line to matplotlib axes with flexible coordinate systems.

    Args:
        ax (plt.Axes): Target axes object to draw on.
        x (np.ndarray | list[float]): X-coordinates of line vertices.
        y (np.ndarray | list[float]): Y-coordinates of line vertices (must match x length).
        style (str, optional): Line style specification:
            - '-': Solid line
            - '--': Dashed line
            - ':': Dotted line
            - '-.': Dash-dot line
            Defaults to '-'.
        linewidth (float, optional): Line width in points. Defaults to 1.
        color (str | None, optional): Line color as matplotlib color spec.
            None uses default color cycle. Defaults to 'black'.
        alpha (float, optional): Transparency (0=transparent, 1=opaque). Defaults to 1.0.
        zorder (int | None, optional): Rendering order (higher values draw on top).
            None uses default layering. Defaults to None.
        transform (str | None, optional): Coordinate system specification:
            - 'data': Data coordinates (default)
            - 'axes': Axes-relative coordinates (0-1)
            - 'figure': Figure-relative coordinates (0-1)
            - 'display': Pixel coordinates
            None defaults to 'data'.
        **kwargs: Additional Line2D properties (e.g., linestyle, label, dash_capstyle).

    Returns:
        Line2D: The created matplotlib line object.

    Raises:
        ValueError: If x and y have different lengths or invalid transform specified.

    Examples:
        >>> # Basic solid line in data coordinates
        >>> line = add_line(ax, [0, 1, 2], [0, 1, 0], color='blue')

        >>> # Dashed line in axes coordinates (relative to axes)
        >>> add_line(ax, [0.1, 0.9], [0.5, 0.5], style='--', transform='axes')

        >>> # Custom styled line with transparency
        >>> add_line(ax, x_data, y_data,
        ...          style='-.', linewidth=2, alpha=0.7,
        ...          color='green')

        >>> # Figure-relative line (spanning entire figure)
        >>> add_line(ax, [0.2, 0.8], [0.1, 0.9], transform='figure')
    """
    # 将输入转换为 numpy 数组
    x = np.asarray(x)
    y = np.asarray(y)

    # 处理坐标变换
    if transform is None or transform == "data":
        transform = ax.transData
    elif transform == "axes":
        transform = ax.transAxes
    elif transform == "figure":
        transform = ax.figure.transFigure
    elif transform == "display":
        transform = None  # 像素坐标
    else:
        raise ValueError(
            "transform must be one of: 'data', 'axes', 'figure', 'display'"
        )

    line = Line2D(
        x,
        y,
        linestyle=style,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        zorder=zorder,
        transform=transform,
        **kwargs,
    )

    ax.add_line(line)

    # 如果采用数据坐标系，则自动缩放
    if transform == ax.transData:
        ax.relim()
        ax.autoscale_view()
