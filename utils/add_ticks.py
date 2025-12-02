"""
add_custom_ticks() can add custom tick lines in axis x or axis y

Author: https://github.com/zbhgis
Last Modified: 2025-07-11
"""

import matplotlib.pyplot as plt
import numpy as np


def add_ticks(
    ax: plt.Axes,
    axis: str = "x",
    origin_viz: bool = False,
    num_ticks: int | None = None,
    positions: list[float] | np.ndarray | None = None,
    color: str = "black",
    linestyle: str = "-",
    linewidth: float = 1,
    ymin: float | None = None,
    ymax: float | None = None,
    xmin: float | None = None,
    xmax: float | None = None,
    clip_on: bool = False,
    **kwargs,
) -> None:
    """Add custom tick lines to matplotlib axes with automatic position handling.

    Args:
        ax (plt.Axes): Target axes object to modify.
        axis (str, optional): Axis to add ticks to, either 'x' or 'y'. Defaults to 'x'.
        origin_viz (bool, optional): If True, sets original tick line length to 0.
            Defaults to False.
        num_ticks (int | None, optional): Number of equally spaced ticks to generate.
            - None: Defaults to 5 when positions is None
            - Ignored when positions is provided
            Defaults to None.
        positions (list[float] | np.ndarray | None, optional): Custom tick positions.
            - Takes precedence over num_ticks when both are provided
            - Defaults to None.
        color (str, optional): Color of tick lines. Defaults to 'black'.
        linestyle (str, optional): Line style of ticks. Common values:
            - '-': Solid line
            - '--': Dashed line
            - ':': Dotted line
            Defaults to '-'.
        linewidth (float, optional): Width of tick lines in points. Defaults to 1.
        ymin (float | None, optional): Start position for x-axis ticks (y-coordinate, 0-1).
            - Only used when axis="x"
            - None defaults to 0.002
            Defaults to None.
        ymax (float | None, optional): End position for x-axis ticks (y-coordinate, 0-1).
            - Only used when axis="x"
            - None defaults to 0.018
            Defaults to None.
        xmin (float | None, optional): Start position for y-axis ticks (x-coordinate, 0-1).
            - Only used when axis="y"
            - None defaults to -0.02
            Defaults to None.
        xmax (float | None, optional): End position for y-axis ticks (x-coordinate, 0-1).
            - Only used when axis="y"
            - None defaults to -0.002
            Defaults to None.
        clip_on (bool, optional): Whether to clip ticks within axes boundaries.
            Defaults to False.
        **kwargs: Additional line properties passed to matplotlib's axvline/axhline.
            Supported arguments include:
            - alpha: Transparency (0-1)
            - dash_capstyle: Style of dash ends
            - solid_capstyle: Style of solid line ends
            - See matplotlib documentation for full list:
              https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axvline.html

    Returns:
        None: Adds tick lines directly to the axes.

    Raises:
        ValueError: If invalid axis type is specified or num_ticks < 2.

    Example:
        >>> # Add dashed red ticks with 50% transparency
        >>> add_custom_ticks(
        ...     ax,
        ...     axis='x',
        ...     positions=[0.2, 0.5, 0.8],
        ...     color='red',
        ...     linestyle='--',
        ...     alpha=0.5,
        ...     dash_capstyle='round'
        ... )
    """
    if axis not in ["x", "y"]:
        raise ValueError("`axis` must be 'x' or 'y'")

    if origin_viz == False:
        ax.tick_params(axis=axis, which="both", length=0)
    else:
        pass

    # 生成刻度位置
    if positions is not None:
        positions = np.asarray(positions)
        if num_ticks is not None:
            # 两个参数都有时，按数量关系动态选择
            if num_ticks <= len(positions):
                positions = positions[:num_ticks]  # 取前num_ticks个
            else:
                pass  # 保留全部positions
    else:
        # 仅num_ticks时生成等间隔刻度
        if num_ticks is None:
            num_ticks = 5  # 默认值
        if num_ticks < 2:
            raise ValueError("`num_ticks` must be at least 2")

        # 获取当前坐标轴范围并生成等分刻度
        if axis == "x":
            xlim = ax.get_xlim()
            positions = np.linspace(xlim[0], xlim[1], num_ticks)
        else:
            ylim = ax.get_ylim()
            positions = np.linspace(ylim[0], ylim[1], num_ticks)

    # 设置默认相对坐标范围
    if axis == "x":
        ymin = ymin if ymin is not None else 0.002
        ymax = ymax if ymax is not None else 0.018
    else:
        xmin = xmin if xmin is not None else 0.002
        xmax = xmax if xmax is not None else 0.018

    # 添加刻度线
    for pos in positions:
        if axis == "x":
            ax.axvline(
                x=pos,
                color=color,
                linestyle=linestyle,
                linewidth=linewidth,
                ymin=ymin,
                ymax=ymax,
                clip_on=clip_on,
                **kwargs,
            )
        else:
            ax.axhline(
                y=pos,
                color=color,
                linestyle=linestyle,
                linewidth=linewidth,
                xmin=xmin,
                xmax=xmax,
                clip_on=clip_on,
                **kwargs,
            )
