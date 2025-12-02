"""
create_subplots() can create subplots in grids and add text

Author: https://github.com/zbhgis
Last Modified: 2025-07-11
"""

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import string


def add_subplots(
    tw: float = 10,
    th: float = 10,
    nrows: int = 2,
    ncols: int = 2,
    gs_loc: (
        list[
            tuple[int | tuple[int, int], int | tuple[int, int]]
            | list[int | tuple[int, int]]
        ]
        | None
    ) = None,
    wspace: float = 0.5,
    hspace: float = 0.4,
    ax_offsets: (
        tuple[float | None, float | None]
        | list[tuple[float | None, float | None] | list[float | None]]
        | None
    ) = None,
    ax_scales: (
        tuple[float | None, float | None]
        | list[tuple[float | None, float | None] | list[float | None]]
        | None
    ) = None,
    ax_scales_anchors: (
        tuple[float | None, float | None]
        | list[tuple[float | None, float | None] | list[float | None]]
        | None
    ) = None,
    text_type: str | None = None,
    text_fix: str | tuple[str, str] | None = None,
    text_index: int | None = None,
    text_step: int = 1,
    text_offsets: (
        tuple[float | None, float | None]
        | list[tuple[float | None, float | None] | list[float | None]]
        | None
    ) = None,
    fontsize: int | str = 20,
    fontweight: int | str = "heavy",
    **text_kwargs,
) -> tuple[plt.Figure, list[plt.Axes]]:
    """Create matplotlib subplots with configurable labels and layout.

    Args:
        tw (float, optional): Total figure width in inches. Defaults to 10.
        th (float, optional): Total figure height in inches. Defaults to 10.
        nrows (int, optional): Number of rows in subplot grid. Defaults to 2.
        ncols (int, optional): Number of columns in subplot grid. Defaults to 2.
        gs_loc (list | None, optional): Subplot location specification. Each element can be:
            - For single subplot: [row, col] or (row, col)
            - For row/column ranges:
                * [row, (col_start, col_end)]  # Row fixed, column range
                * [(row_start, row_end), col]  # Column fixed, row range
                * [(row_start, row_end), (col_start, col_end)]  # Both ranges
            Examples:
                - [0, 1]                      # Single subplot at row 0, column 1
                - [1, (2, 4)]                 # Row 1, columns 2-4
                - [(0, 2), 3]                 # Rows 0-2, column 3
                - [(1, 3), (0, 2)]            # Rows 1-3 and columns 0-2
            Defaults to None (auto-fill all grid positions).
        wspace (float, optional): Width space between subplots as fraction of axis width.
            Defaults to 0.5.
        hspace (float, optional): Height space between subplots as fraction of axis height.
            Defaults to 0.4.
        ax_offsets (tuple | list | None, optional): Axis position offsets in figure coordinates.
            Can be either:
            - Tuple: Uniform offset for all subplots (x_offset, y_offset)
            - List: Individual offsets per subplot
            Defaults to None.
        ax_scales (tuple | list | None, optional): Axis scaling factors. Can be either:
            - Tuple: Uniform scale for all subplots (x_scale, y_scale)
            - List: Individual scales per subplot
            Defaults to None.
        ax_scales_anchors (tuple | list | None, optional): Scaling anchor points. Can be either:
            - Tuple: Uniform anchor for all subplots (x_anchor, y_anchor)
            - List: Individual anchors per subplot
            Defaults to None.
        text_type (str | None, optional): Label type specification. One of:
            - 'a': Lowercase alphabetical labels
            - 'A': Uppercase alphabetical labels
            - '1': Numerical labels
            - None: No labels
            Defaults to None.
        text_fix (str | tuple | None, optional): Label prefix/suffix configuration. Can be:
            - None: No affixes
            - str: Single character prefix or split at text_index
            - tuple: Explicit (prefix, suffix) pair
            Defaults to None.
        text_index (int | None, optional): Split position for text_fix string.
            Defaults to None (auto-determined).
        text_step (int, optional): Spacing interval between labels. Defaults to 1.
        text_offsets (tuple | list | None, optional): Label position offsets in axis coordinates.
            Can be either:
            - Tuple: Uniform offset for all labels (x_offset, y_offset)
            - List: Individual offsets per label
            Defaults to None.
        fontsize (int | str, optional): Label font size. Defaults to 20.
        fontweight (int | str, optional): Label font weight. Defaults to 'heavy'.
        **text_kwargs: Additional text properties passed to matplotlib.text.Text.

    Returns:
        tuple[plt.Figure, list[plt.Axes]]:
            - Figure: The created matplotlib Figure object
            - Axes: List of Axes objects for each subplot

    Raises:
        ValueError: If invalid grid specifications or text parameters are provided.

    Example:
        >>> # Basic 2x2 grid with automatic labels
        >>> fig, axes = add_subplots()

        >>> # Complex grid with custom labels
        >>> fig, axes = add_subplots(
        ...     gs_loc=[[0, (0, 5)], [0, (6, 11)], [1, (2, 10)]],
        ...     tw=8,
        ...     th=8,
        ...     nrows=2,
        ...     ncols=12,
        ...     wspace=0.6,
        ...     hspace=0.3,
        ...     ax_offsets=[[-0.07, -0.01]],
        ...     ax_scales=[[1.1, 1.1]],
        ...     ax_scales_anchors=[[0, 1]],
        ...     text_type="e",
        ...     text_fix="()",
        ...     text_index=1,
        ...     text_offsets=[
        ...         [-0.15, 1.15],
        ...         [-0.15, 1.15],
        ...         [-0.1, 1.15],
        ...     ],
        ...     text_step=1,
        ...     fontsize=14,
        ...     fontweight="bold",
        ... )
    """

    # 创建图形
    fig = plt.figure(figsize=(tw, th))
    # 设置子图及其间距
    gs = GridSpec(nrows, ncols, figure=fig, wspace=wspace, hspace=hspace)
    # 创建子图列表
    ax_list = []
    # 默认情况自动生成
    if gs_loc is None:
        for i in range(nrows):
            for j in range(ncols):
                ax = fig.add_subplot(gs[i, j])
                ax_list.append(ax)
    else:
        for loc in gs_loc:
            # 参数校验
            if not isinstance(loc, (list, tuple)) or len(loc) != 2:
                raise ValueError(
                    "Value must be [row, col] or [row, (row_start, row_end)] or [col, (col_start, col_end)]"
                )

            # 统一转换为切片格式
            row_spec = _to_slice(loc[0])
            col_spec = _to_slice(loc[1])
            ax = fig.add_subplot(gs[row_spec, col_spec])
            ax_list.append(ax)

    # 子图偏移
    ax_offsets_list = _get_vars(len(ax_list), ax_offsets)
    for ax, offset in zip(ax_list, ax_offsets_list):
        pos = ax.get_position()
        ax.set_position(
            [pos.x0 + offset[0], pos.y0 + offset[1], pos.x1 - pos.x0, pos.y1 - pos.y0]
        )

    # 子图缩放
    ax_scales_list = _get_vars(len(ax_list), ax_scales, (1, 1))
    ax_scales_anchors_list = _get_vars(len(ax_list), ax_scales_anchors, (0, 1))

    _apply_scale(ax_list, ax_scales_list, ax_scales_anchors_list)

    # 文本标签
    if text_type is not None:
        # 生成文本
        labels = _get_text(nrows, ncols, text_type, text_fix, text_index, text_step)

        # 获取文本标签偏移量
        text_offsets_list = _get_vars(len(ax_list), text_offsets, (0, 1))

        # 文本标签其他参数
        text_params = {
            "fontsize": fontsize,
            "fontweight": fontweight,
            "ha": text_kwargs.pop("ha", "right"),
            "va": text_kwargs.pop("va", "bottom"),
            **text_kwargs,
        }

        # 添加左上角标签
        for ax, label, offset in zip(ax_list, labels, text_offsets_list):
            ax.text(
                offset[0],
                offset[1],
                label,
                transform=ax.transAxes,
                **text_params,
            )

    # text_type为None则不设置标签文本
    else:
        pass

    return fig, ax_list


def _to_slice(spec):
    """Convert a number or tuple to a slice object.

    Args:
        spec (int or tuple): Input specification, which can be:
            - Single integer (converted to slice(n, n+1))
            - 2-element tuple (converted to slice(start, end))

    Returns:
        slice: The converted slice object

    Examples:
        >>> # Convert single integer
        >>> _to_slice(5)
        slice(5, 6, None)

        >>> # Convert tuple
        >>> _to_slice((2, 8))
        slice(2, 8, None)
    """
    if isinstance(spec, int):
        return slice(spec, spec + 1)
    elif isinstance(spec, tuple):
        return slice(spec[0], spec[1])


def _get_vars(
    nplots: int,
    input_vars: (
        tuple[float | None, float | None]
        | list[tuple[float | None, float | None] | list[float | None]]
        | None
    ) = None,
    default_vars: tuple[float, float] = (0, 0),
) -> list[tuple[float, float]]:
    """Normalize and validate variables input for multiple subplots.

    Args:
        nplots (int): Number of subplots required (must be positive integer).
        input_vars (tuple | list | None, optional): Input variables specification:
            - None: Use default variables for all subplots
            - tuple[float, float]: Unified (x,y) variables for all subplots
            - list[tuple | list]: Individual variables per subplot where each element is:
                * tuple[float, float]: (x,y) coordinates
                * list[float]: [x,y] coordinates
            None values in tuples/lists will be replaced with defaults.
            Defaults to None.
        default_vars (tuple[float, float], optional): Default (x,y) values used when:
            - input_vars is None
            - input_vars contains None values
            Defaults to (0, 0).

    Returns:
        list[tuple[float, float]]: Normalized (x,y) coordinate tuples for each subplot,
        guaranteed to contain no None values.

    Raises:
        ValueError: If input_vars format is invalid or length doesn't match nplots.

    Examples:
        >>> # Default variables case
        >>> _get_vars(3, None)
        [(0, 0), (0, 0), (0, 0)]

        >>> # Unified variables with None handling
        >>> _get_vars(2, (1.5, None), default_vars=(0, 1))
        [(1.5, 1), (1.5, 1)]

        >>> # Individual variables with mixed formats
        >>> _get_vars(3, [(1,2), None, [3,4]])
        [(1, 2), (0, 0), (3, 4)]

        >>> # Automatic padding with defaults
        >>> _get_vars(4, [[1,2], [3,4]])
        [(1, 2), (3, 4), (0, 0), (0, 0)]

        >>> # Error case (invalid format)
        >>> _get_vars(2, [1, 2, 3])  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Invalid variable format: [1, 2, 3]
    """
    # Handle None case
    if input_vars is None:
        return [default_vars] * nplots

    # Handle unified variables
    elif (
        isinstance(input_vars, (tuple, list))
        and len(input_vars) == 2
        and all(isinstance(x, (int, float, type(None))) for x in input_vars)
    ):
        x = default_vars[0] if input_vars[0] is None else input_vars[0]
        y = default_vars[1] if input_vars[1] is None else input_vars[1]
        return [(x, y)] * nplots

    # Handle individual variables list
    elif isinstance(input_vars, list):
        processed_vars = []

        for var in input_vars:
            # Handle None case
            if var is None:
                processed_vars.append(default_vars)
                continue

            # Handle tuple/list format variables
            if isinstance(var, (tuple, list)) and len(var) == 2:
                # Handle None values
                x = default_vars[0] if var[0] is None else var[0]
                y = default_vars[1] if var[1] is None else var[1]
                processed_vars.append((x, y))
            else:
                raise ValueError(f"Invalid variable format: {var}")

        # Pad with defaults if needed
        if len(processed_vars) < nplots:
            processed_vars.extend([default_vars] * (nplots - len(processed_vars)))

        return processed_vars

    raise ValueError(f"Invalid input_vars type: {type(input_vars)}")


def _apply_scale(
    ax_list: list[plt.Axes],
    ax_scales_list: list[tuple[float, float]],
    ax_scales_anchors_list: list[tuple[float, float]],
) -> None:
    """Apply scaling transformations to matplotlib axes with anchor-based positioning.

    Args:
        ax_list (list[plt.Axes]): List of Axes objects to scale.
        ax_scales_list (list[tuple[float, float]]): List of scaling factors where each tuple contains:
            - width_scale: Horizontal scaling factor
            - height_scale: Vertical scaling factor (currently uses width_scale for both dimensions)
        ax_scales_anchors_list (list[tuple[float, float]]): List of anchor points defining the scaling
            reference position for each Axes. Valid anchor combinations:
            - (0, 0): Scale from bottom-left corner
            - (0, 1): Scale from top-left corner
            - (1, 0): Scale from bottom-right corner
            - (1, 1): Scale from top-right corner

    Returns:
        None: Modifies Axes objects in-place.

    Raises:
        ValueError: If any anchor value is not one of the valid combinations.

    Examples:
        >>> # Scale axes from their bottom-left corners
        >>> _apply_scale(
        ...     ax_list=[ax1, ax2],
        ...     ax_scales_list=[(1.5, 1.5), (0.8, 0.8)],
        ...     ax_scales_anchors_list=[(0, 0), (0, 0)]
        ... )

        >>> # Scale axes from different anchor points
        >>> _apply_scale(
        ...     ax_list=[ax1, ax2, ax3],
        ...     ax_scales_list=[(2.0, 2.0), (1.2, 1.2), (0.5, 0.5)],
        ...     ax_scales_anchors_list=[(0, 0), (1, 1), (0, 1)]
        ... )
    """
    for ax, scale, anchor in zip(ax_list, ax_scales_list, ax_scales_anchors_list):
        pos = ax.get_position()
        new_width = pos.width * scale[0]
        new_height = pos.height * scale[0]

        # Calculate new position based on anchor point
        if anchor == (0, 0):
            new_x0, new_y0 = pos.x0, pos.y0
        elif anchor == (0, 1):
            new_x0, new_y0 = pos.x0, pos.y1 - new_height
        elif anchor == (1, 0):
            new_x0, new_y0 = pos.x1 - new_width, pos.y0
        elif anchor == (1, 1):
            new_x0, new_y0 = pos.x1 - new_width, pos.y1 - new_height
        else:
            raise ValueError(
                f"Invalid anchor parameter: {anchor}. "
                "Valid values are (0,0), (0,1), (1,0), or (1,1)"
            )

        # Apply new position and dimensions
        ax.set_position([new_x0, new_y0, new_width, new_height])


def _get_text(
    nrows: int,
    ncols: int,
    text_type: str,
    text_fix: str | tuple[str, str] | None,
    text_index: int | None,
    text_step: int,
    max_num: int | None = None,
) -> list[str]:
    """Generate text labels for subplots with configurable formatting.

    Args:
        nrows (int): Number of rows in subplot grid (must be ≥ 1).
        ncols (int): Number of columns in subplot grid (must be ≥ 1).
        text_type (str): Base label type specification:
            - 'a'-'z': Lowercase alphabetical sequence
            - 'A'-'Z': Uppercase alphabetical sequence
            - '1'-'9': Numerical sequence
            - Other: Defaults to lowercase letters
        text_fix (str | tuple[str, str] | None): Prefix/suffix configuration:
            - None: No affixes
            - str: Split into prefix/suffix at text_index
            - tuple[str, str]: Explicit (prefix, suffix) pair
        text_index (int | None): Split position for text_fix string when str is provided.
            None defaults to middle position.
        text_step (int): Label spacing interval (≥1):
            - 1: Continuous labels
            - 2: Every other label with empty strings between
            - N: N-1 empty strings between labels
        max_num (int | None, optional): Maximum number for numerical sequences.
            None defaults to 26. Ignored for non-numeric text_type.

    Returns:
        list[str]: Generated labels with specified formatting.

    Raises:
        ValueError: If invalid text_type or text_step < 1 is provided.

    Examples:
        >>> # Basic alphabetical sequence
        >>> _get_text(2, 2, 'a', None, None, 1)
        ['a', 'b', 'c', 'd']

        >>> # Numerical sequence with prefix
        >>> _get_text(1, 3, '1', ('Item-', ''), None, 1, 10)
        ['Item-1', 'Item-2', 'Item-3']

        >>> # Formatted labels with spacing
        >>> _get_text(1, 3, 'A', ('(', ')'), None, 2)
        ['(A)', '', '(B)', '', '(C)']

        >>> # Mixed format with custom split
        >>> _get_text(2, 1, 'x', 'pre_text', 3, 1)
        ['pre', 'x', 'text', 'pre', 'y', 'text']
    """

    total_subplots = nrows * ncols
    labels = []
    # 处理字母标签（小写）
    if text_type.islower() and text_type in string.ascii_lowercase:
        start_idx = string.ascii_lowercase.index(text_type)
        available_chars = string.ascii_lowercase[start_idx:]

        for i in range(total_subplots):
            if i < len(available_chars):
                labels.append(available_chars[i])
            else:
                labels.append(available_chars[-1])  # 超出后用 'z'
    # 处理字母标签（大写）
    elif text_type.isupper() and text_type in string.ascii_uppercase:
        start_idx = string.ascii_uppercase.index(text_type)
        available_chars = string.ascii_uppercase[start_idx:]

        for i in range(total_subplots):
            if i < len(available_chars):
                labels.append(available_chars[i])
            else:
                labels.append(available_chars[-1])  # 超出后用 'Z'
    # 处理数字标签
    elif text_type.isdigit():
        start_num = int(text_type)
        if max_num is None:
            max_num = 26

        for i in range(total_subplots):
            current_num = start_num + i
            if current_num <= max_num:
                labels.append(str(current_num))
            else:
                labels.append(str(max_num))  # 超出后用最大数字
    # 其他无法识别的情况
    else:
        labels = list(string.ascii_lowercase[:total_subplots])

    # 处理前后缀
    if text_fix is not None:
        text_index = text_index if text_index is not None else 1
        prefix, suffix = text_fix[:text_index], text_fix[text_index:]

        labels = [f"{prefix}{label}{suffix}" for label in labels]

    # 处理文本生成间隔
    if text_step == 1 or text_step is None:
        return labels

    new_labels = []
    for i, label in enumerate(labels):
        new_labels.append(label)
        # 在非末尾位置插入指定数量的空字符串
        if i != len(labels) - 1:
            new_labels.extend([""] * (text_step - 1))
    return new_labels
