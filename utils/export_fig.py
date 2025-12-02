"""
export_fig() can export different image types quickly

Author: https://github.com/zbhgis
Last Modified: 2025-06-30
"""

import matplotlib.pyplot as plt
import inspect
import os


def export_fig(
    formats: str | list[str] | None = None,
    output_path: str | None = None,
    dpi: int = 300,
    bbox_inches: str | None = "tight",
) -> None:
    """Export current matplotlib figure to image file(s).

    Args:
        formats (str | list[str] | None, optional): Image format(s) to export.
            Supported formats:
            - 'png': Portable Network Graphics
            - 'jpg': JPEG image
            - 'bmp': Bitmap image
            - 'pdf': Portable Document Format
            - 'svg': Scalable Vector Graphics
            - 'tiff': Tagged Image File Format
            - 'eps': Encapsulated PostScript
            Can be either a single format string or list of formats.
            Defaults to ['jpg'].
        output_path (str | None, optional): Output file path without extension.
            If None, uses the caller script's path and name.
            Defaults to None.
        dpi (int, optional): Dots per inch for raster formats (png/jpg/tiff).
            Defaults to 300.
        bbox_inches (str | None, optional): Bounding box in inches.
            - 'tight': Automatically trim whitespace
            - None: Disable trimming
            Defaults to 'tight'.

    Returns:
        None: Outputs files to specified location.

    Raises:
        ValueError: If invalid image format is specified.

    Examples:
        >>> # Export to single format
        >>> export_fig(formats='png', output_path='output/figure')

        >>> # Export to multiple formats
        >>> export_fig(formats=['png', 'pdf'], output_path='output/figure', dpi=600)

        >>> # Use default filename and format
        >>> export_fig()
    """
    # 设置输出格式
    if formats is None:
        formats = ["jpg"]
    elif isinstance(formats, str):
        formats = [formats]

    # 设置导出路径为调用文件的路径和名称
    if output_path is None:
        caller_frame = inspect.stack()[1]
        caller_filepath = caller_frame.filename
        caller_filename = os.path.splitext(os.path.basename(caller_filepath))[0]
        output_path = os.path.join(os.path.dirname(caller_filepath), caller_filename)
    else:
        output_path = os.path.splitext(output_path)[0]

    # 设置不同的绘图参数
    format_params = {
        "png": {"dpi": dpi},
        "jpg": {"dpi": dpi},
        "bmp": {},
        "pdf": {},
        "svg": {},
        "tiff": {"dpi": dpi},
        "eps": {},
    }

    # 依次导出各个图片格式
    for fmt in formats:
        if fmt.lower() not in format_params:
            print(f"Unsupported format: '{fmt}'. Skipping export.")
            continue

        filename = f"{output_path}.{fmt.lower()}"
        params = {**format_params[fmt.lower()]}
        if bbox_inches:
            params["bbox_inches"] = bbox_inches

        plt.savefig(filename, format=fmt.lower(), **params)
