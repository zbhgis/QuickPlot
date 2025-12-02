"""
set_common_options() can create subplots in grids and add text

Author: https://github.com/zbhgis
Last Modified: 2025-07-11
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def format_ticks(
    ax: plt.Axes,
    *,
    x_zero_format: bool = False,
    y_zero_format: bool = False,
    x_precision: int | None = None,
    y_precision: int | None = None,
    x_scientific: bool | None = None,
    y_scientific: bool | None = None,
    x_prefix: str = "",
    y_prefix: str = "",
    x_suffix: str = "",
    y_suffix: str = "",
    x_thousands: bool = False,
    y_thousands: bool = False,
) -> None:
    """Configure advanced tick formatting options for matplotlib axes.

    Args:
        ax (plt.Axes): Target matplotlib Axes object to format.
        x_zero_format (bool, optional): If True, explicitly formats x-axis zero ticks.
            Defaults to False.
        y_zero_format (bool, optional): If True, explicitly formats y-axis zero ticks.
            Defaults to False.
        x_precision (int | None, optional): Number of decimal places for x-axis ticks.
            When None (default), maintains the original formatting.
        y_precision (int | None, optional): Number of decimal places for y-axis ticks.
            When None (default), maintains the original formatting.
        x_scientific (bool | None, optional): Controls scientific notation on x-axis:
            - True: Forces scientific notation
            - False: Disables scientific notation
            - None (default): Keeps matplotlib's auto-detection
        y_scientific (bool | None, optional): Controls scientific notation on y-axis:
            - True: Forces scientific notation
            - False: Disables scientific notation
            - None (default): Keeps matplotlib's auto-detection
        x_prefix (str, optional): String to prepend to all x-axis tick labels.
            Defaults to "".
        y_prefix (str, optional): String to prepend to all y-axis tick labels.
            Defaults to "".
        x_suffix (str, optional): String to append to all x-axis tick labels.
            Defaults to "".
        y_suffix (str, optional): String to append to all y-axis tick labels.
            Defaults to "".
        x_thousands (bool, optional): If True, adds comma separators to x-axis values.
            Defaults to False.
        y_thousands (bool, optional): If True, adds comma separators to y-axis values.
            Defaults to False.

    Returns:
        None: Modifies the Axes object in-place.

    Examples:
        >>> fig, ax = plt.subplots()
        >>> format_ticks(ax,
        ...              x_zero_format=True,
        ...              y_precision=2,
        ...              y_thousands=True,
        ...              y_suffix=" units")
    """

    def create_formatter(
        zero_format: bool,
        precision: int | None,
        scientific: bool | None,
        prefix: str,
        suffix: str,
        thousands_separator: bool,
    ) -> ticker.Formatter:
        """Factory function for tick formatters"""

        def format_func(value, _):
            # 处理零格式
            if zero_format and abs(value) < 1e-10:
                return f"{prefix}0{suffix}"

            # 处理科学计数法
            if scientific is not None and scientific:
                fmt = f".{precision}e" if precision is not None else "e"
                s = format(value, fmt)
            else:
                if precision is not None:
                    # 整数的特殊处理
                    if precision == 0:
                        s = f"{int(round(value))}"
                    else:
                        s = f"{value:.{precision}f}"
                else:
                    # 自动检测最佳格式
                    s = str(value)
                    if "." in s:
                        s = s.rstrip("0").rstrip(".") if s.endswith("0") else s

            # 如果启用，则应用千位分隔符
            if thousands_separator and (scientific is None or not scientific):
                if "e" not in s:  
                    parts = s.split(".")
                    # 用逗号分隔整数部分
                    if parts[0].lstrip("-").isdigit():
                        parts[0] = "{:,}".format(int(parts[0]))
                    s = ".".join(parts) if len(parts) > 1 else parts[0]

            return f"{prefix}{s}{suffix}"

        return ticker.FuncFormatter(format_func)

    # 配置x轴
    if any(
        [
            x_zero_format,
            x_precision is not None,
            x_scientific is not None,
            x_prefix,
            x_suffix,
            x_thousands,
        ]
    ):
        ax.xaxis.set_major_formatter(
            create_formatter(
                x_zero_format,
                x_precision,
                x_scientific,
                x_prefix,
                x_suffix,
                x_thousands,
            )
        )

    # 配置y轴
    if any(
        [
            y_zero_format,
            y_precision is not None,
            y_scientific is not None,
            y_prefix,
            y_suffix,
            y_thousands,
        ]
    ):
        ax.yaxis.set_major_formatter(
            create_formatter(
                y_zero_format,
                y_precision,
                y_scientific,
                y_prefix,
                y_suffix,
                y_thousands,
            )
        )
