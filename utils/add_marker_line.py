"""
add_marker_line() can add custom marked lines in ax

Author: https://github.com/zbhgis
Last Modified: 2025-07-13
"""

import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import ArrayLike
from typing import Any


def add_marker_line(
    ax: plt.Axes,
    x_point: ArrayLike | list[float] | tuple[float, ...],
    y_point: ArrayLike | list[float] | tuple[float, ...],
    line_density: int = 10,
    line_mode: str = "single",
    style: str | list[str] = "o",
    size: float | list[float] = 2,
    edgecolor: str | list[str] = "#1F77B4",
    edgewidth: float | list[float] = 0,
    facecolor: str | list[str] = "#1F77B4",
    facecoloralt: str | list[str] = "#F07775",
    markevery: int | list[int] | None = None,
    fillstyle: str | list[str] = "full",
    alpha: float | list[float] = 1,
    linestyle: str = "none",
    clip_on: bool = True,
    point_mode: str = "single",
    point_style: str | list[str] = "s",
    point_size: float | list[float] = 0,
    point_edgecolor: str | list[str] = "#1F77B4",
    point_edgewidth: float | list[float] = 0,
    point_facecolor: str | list[str] = "#1F77B4",
    point_facecoloralt: str | list[str] = "#F07775",
    point_markevery: int | list[int] | None = None,
    point_fillstyle: str | list[str] = "full",
    point_alpha: float | list[float] = 1,
    **kwargs,
) -> None:
    """Add a customizable line with markers to matplotlib axes.

    Args:
        ax (plt.Axes): Target axes object for drawing.
        x_point (ArrayLike | list[float] | tuple[float, ...]): X-coordinates for points/lines.
        y_point (ArrayLike | list[float] | tuple[float, ...]): Y-coordinates for points/lines.
        line_density (int, optional): Marker density along line (points/unit length).
            Defaults to 10.
        line_mode (str, optional): Marker distribution pattern:
            - 'single': Evenly spaced individual markers
            - 'group-start': Marker clusters at line start
            - 'group-end': Marker clusters at line end
            Defaults to 'single'.
        style (str | list[str], optional): Marker style specification. Common values:
            - 'o': Circle
            - 's': Square
            - '^': Triangle up
            - See matplotlib.markers for full list
            Defaults to 'o'.
        size (float | list[float], optional): Marker size in points. Defaults to 2.
        edgecolor (str | list[str], optional): Marker edge color. Defaults to '#1F77B4'.
        edgewidth (float | list[float], optional): Marker edge width. Defaults to 0.
        facecolor (str | list[str], optional): Marker face color. Defaults to '#1F77B4'.
        facecoloralt (str | list[str], optional): Alternate face color for unfilled markers.
            Defaults to '#F07775'.
        markevery (int | list[int] | None, optional): Marker frequency (e.g., 2=every other point).
            Defaults to None.
        fillstyle (str | list[str], optional): Marker fill style:
            - 'full': Solid fill
            - 'left'/'right': Half-filled
            - 'none': No fill
            Defaults to 'full'.
        alpha (float | list[float], optional): Marker transparency (0=transparent, 1=opaque).
            Defaults to 1.
        linestyle (str, optional): Line style between markers:
            - '-': Solid
            - '--': Dashed
            - ':': Dotted
            - 'none': No line
            Defaults to 'none'.
        clip_on (bool, optional): Clip markers to axes bounds. Defaults to True.
        point_mode (str, optional): Additional point distribution mode. Same options as line_mode.
            Defaults to 'single'.
        point_style (str | list[str], optional): Additional point marker style. Defaults to 's'.
        point_size (float | list[float], optional): Additional point size. Defaults to 0.
        point_edgecolor (str | list[str], optional): Additional point edge color.
            Defaults to '#1F77B4'.
        point_edgewidth (float | list[float], optional): Additional point edge width. Defaults to 0.
        point_facecolor (str | list[str], optional): Additional point face color.
            Defaults to '#1F77B4'.
        point_facecoloralt (str | list[str], optional): Alternate color for additional points.
            Defaults to '#F07775'.
        point_markevery (int | list[int] | None, optional): Additional point frequency.
            Defaults to None.
        point_fillstyle (str | list[str], optional): Additional point fill style.
            Defaults to 'full'.
        point_alpha (float | list[float], optional): Additional point transparency.
            Defaults to 1.
        **kwargs: Additional line properties passed to matplotlib.plot().

    Returns:
        None: Modifies the Axes object in-place.

    Raises:
        ValueError: If invalid mode specified or coordinate arrays mismatch in length.

    Examples:
        >>> # Basic line with circle markers
        >>> x = np.linspace(0, 10, 100)
        >>> y = np.sin(x)
        >>> add_marker_line(ax, x, y)

        >>> # Grouped markers with custom styles
        >>> add_marker_line(
        ...     ax, x, y,
        ...     line_mode='group-start',
        ...     style=['o', 's', '^'],
        ...     facecolor=['red', 'green', 'blue'],
        ...     line_density=15
        ... )

        >>> # Line with secondary points
        >>> add_marker_line(
        ...     ax, x, y,
        ...     point_mode='group-end',
        ...     point_style='D',
        ...     point_size=6,
        ...     point_facecolor='gold'
        ... )
    """
    x_point = np.asarray(x_point)
    y_point = np.asarray(y_point)

    if len(x_point) != len(y_point):
        raise ValueError(
            f"x_point and y_point must have same length, got {len(x_point)} and {len(y_point)}"
        )

    # 直线模式
    if len(x_point) == 2 and len(y_point) == 2:
        length = np.sqrt(
            (x_point[1] - x_point[0]) ** 2 + (y_point[1] - y_point[0]) ** 2
        )
        num_points = max(2, int(line_density * length))
        x_line = np.linspace(x_point[0], x_point[1], num_points)
        y_line = np.linspace(y_point[0], y_point[1], num_points)
    # 按曲线长度计算密度
    else:
        segments = np.sqrt(np.diff(x_point) ** 2 + np.diff(y_point) ** 2)
        total_length = np.sum(segments)
        num_points = max(2, int(total_length * line_density))
        t = np.cumsum(np.r_[0, segments]) / total_length  # 归一化曲线长度参数
        t_new = np.linspace(0, 1, num_points)
        x_line = np.interp(t_new, t, x_point)
        y_line = np.interp(t_new, t, y_point)

    line_params = {
        "style": style,
        "size": size,
        "edgecolor": edgecolor,
        "edgewidth": edgewidth,
        "facecolor": facecolor,
        "facecoloralt": facecoloralt,
        "markevery": markevery,
        "fillstyle": fillstyle,
        "alpha": alpha,
    }

    # 绘制标记线
    line_res_params, line_value_len = _align_params(line_params)
    for i in range(line_value_len):
        x_line_new, y_line_new = _set_mode(x_line, y_line, line_mode, i, line_value_len)

        ax.plot(
            x_line_new,
            y_line_new,
            marker=line_res_params["style"][i],
            markersize=line_res_params["size"][i],
            markeredgecolor=line_res_params["edgecolor"][i],
            markeredgewidth=line_res_params["edgewidth"][i],
            markerfacecolor=line_res_params["facecolor"][i],
            markerfacecoloralt=line_res_params["facecoloralt"][i],
            markevery=line_res_params["markevery"][i],
            fillstyle=line_res_params["fillstyle"][i],
            alpha=line_res_params["alpha"][i],
            linestyle=linestyle,
            clip_on=clip_on,
            **kwargs,
        )

    # 绘制额外标记点
    point_params = {
        "point_style": point_style,
        "point_size": point_size,
        "point_edgecolor": point_edgecolor,
        "point_edgewidth": point_edgewidth,
        "point_facecolor": point_facecolor,
        "point_facecoloralt": point_facecoloralt,
        "point_markevery": point_markevery,
        "point_fillstyle": point_fillstyle,
        "point_alpha": point_alpha,
    }

    point_res_params, point_value_len = _align_params(point_params)
    for i in range(point_value_len):
        x_point_new, y_point_new = _set_mode(
            x_point, y_point, point_mode, i, point_value_len
        )
        ax.plot(
            x_point_new,
            y_point_new,
            marker=point_res_params["point_style"][i],
            markersize=point_res_params["point_size"][i],
            markeredgecolor=point_res_params["point_edgecolor"][i],
            markeredgewidth=point_res_params["point_edgewidth"][i],
            markerfacecolor=point_res_params["point_facecolor"][i],
            markerfacecoloralt=point_res_params["point_facecoloralt"][i],
            markevery=point_res_params["point_markevery"][i],
            fillstyle=point_res_params["point_fillstyle"][i],
            alpha=point_res_params["point_alpha"][i],
            linestyle="none",
            clip_on=clip_on,
        )


def _align_params(params: dict[str, Any]) -> tuple[dict[str, list[Any]], int]:
    """Convert input parameters to length-aligned lists for consistent plotting.

    Args:
        params (dict[str, Any]): Input parameters dictionary where values can be:
            - Single values (scalars, strings, etc.)
            - Sequences (list, tuple, np.ndarray)
            Strings are always treated as single values (never split into characters).

    Returns:
        tuple[dict[str, list[Any]], int]:
            - dict[str, list[Any]]: Processed parameters with all values converted to lists
              of equal length by repeating shorter sequences as needed.
            - int: The maximum length among all parameter sequences (before alignment).

    Raises:
        ValueError: If params is empty or contains invalid sequence combinations.

    Examples:
        >>> # Single values become repeated lists
        >>> _align_params({'color': 'red', 'size': 10})

        >>> # Mixed single values and sequences
        >>> _align_params({'style': ['o', 's'], 'alpha': 0.5})

        >>> # Complex alignment case
        >>> _align_params({
        ...     'marker': ['o', 's', '^'],
        ...     'color': ['red', 'blue'],
        ...     'size': 10
        ... })
    """

    def _to_list(value: Any) -> list:
        """将输入值转换为列表，保护字符串不被拆分"""
        if isinstance(value, str):  
            return [value]
        elif isinstance(value, (list, tuple, np.ndarray)):
            return list(value)
        else:  
            return [value]

    # 统一转为列表
    list_params = {k: _to_list(v) for k, v in params.items()}

    # 计算最大长度
    max_len = max(len(v) for v in list_params.values()) if list_params else 1

    # 长度对齐
    result_params = {}
    for key, value in list_params.items():
        result_params[key] = (
            value
            if len(value) >= max_len
            else [value[i % len(value)] for i in range(max_len)]
        )

    return result_params, max_len


def _set_mode(
    x: ArrayLike | list[float] | tuple[float, ...],
    y: ArrayLike | list[float] | tuple[float, ...],
    input_mode: str,
    i: int,
    value_len: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Select and return a subset of points based on the specified distribution mode.

    Args:
        x (ArrayLike | list[float] | tuple[float, ...]): Input x-coordinates.
            Can be any array-like object compatible with matplotlib (numpy array,
            list, tuple, or single value which will be converted to array).
        y (ArrayLike | list[float] | tuple[float, ...]): Input y-coordinates.
            Must be same length and type as x-coordinates.
        input_mode (str): Point selection distribution mode. Valid options:
            - 'single': Select every value_len-th point (index % value_len == i)
            - 'group-start': Divide into value_len equal groups, selecting ith group
              with extra points added to the first groups if uneven division
            - 'group-end': Divide into value_len equal groups, selecting ith group
              with extra points added to the last groups if uneven division
        i (int): Current group index to select (0-based, must be < value_len).
        value_len (int): Total number of groups to divide points into.

    Returns:
        tuple[np.ndarray, np.ndarray]: Selected subset of (x, y) coordinates as numpy arrays.

    Raises:
        ValueError: If input_mode is invalid, or x/y have different lengths.
        IndexError: If i >= value_len (group index out of bounds).

    Examples:
        >>> x = np.arange(10)
        >>> y = x**2

        >>> # Select every 3rd point starting at index 1
        >>> _set_mode(x, y, 'single', 1, 3)

        >>> # Get second group of 3 with extra points at start
        >>> _set_mode(x, y, 'group-start', 1, 3)

        >>> # Get first group of 3 with extra points at end
        >>> _set_mode(x, y, 'group-end', 0, 3)
    """

    if input_mode == "single" or input_mode is None:
        # 单点模式：选取所有索引满足 (idx % max_len == i) 的点
        mask = [idx % value_len == i for idx in range(len(x))]
        x_new = x[mask]
        y_new = y[mask]
    elif input_mode == "group-start":
        # 分组模式：按max_len均分点（当有余数时，第一组更多）
        x_new = np.array_split(x, value_len)[i]
        y_new = np.array_split(y, value_len)[i]
    elif input_mode == "group-end":
        # 分组模式：按max_len均分点（当有余数时，最后一组更多）
        group_size = len(x) // value_len
        remainder = len(x) % value_len
        start = i * group_size + max(0, i - (value_len - remainder))
        end = start + group_size + (1 if i >= (value_len - remainder) else 0)

        x_new = x[start:end]
        y_new = y[start:end]
    else:
        raise ValueError(
            "point_mode must be one of: 'single', 'group-start', 'group-end'"
        )
    return x_new, y_new
