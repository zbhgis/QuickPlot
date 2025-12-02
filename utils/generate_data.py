"""
generate_data() can export different data randomly

Author: https://github.com/zbhgis
Last Modified: 2025-07-03
"""

import csv
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import math
from typing import Any


def generate_data(
    output_path: str | Path,
    num_samples: int,
    fields_config: list[dict[str, Any]],
    random_seed: int | None = None,
    overwrite: bool = False,
    delimiter: str = ",",
    quotechar: str = '"',
) -> None:
    """Generate CSV files with configurable random data.

    Args:
        output_path (str | Path): Path to the output CSV file. Supports both string
            and Path object representations.
        num_samples (int): Number of records to generate in the output file.
        fields_config (list[dict[str, Any]]): Field configuration list where each dictionary
            contains field specifications. Each dict must include:
            - name (str): Required field name
            - type (str): Required field type. Supported types:
                'int', 'float', 'string', 'date', 'bool', 'choice'
            - min (int | float | None): Minimum value for numeric types
            - max (int | float | None): Maximum value for numeric types
            - length (int | None): String length for 'string' type
            - start_date (str | None): Start date for 'date' type (format: 'YYYY-MM-DD')
            - end_date (str | None): End date for 'date' type (format: 'YYYY-MM-DD')
            - choices (list[Any] | None): Options for 'choice' type
            - weights (list[float] | None): Probability weights for choices
            - format (str | None): Date format string (default: '%Y-%m-%d')
            - charset (str | None): Character set for 'string' type (default: ascii_letters)
            - prefix (str | None): String prefix
            - suffix (str | None): String suffix
            - decimals (int | None): Decimal places for 'float' type (default: 2)
        random_seed (int | None, optional): Seed value for reproducible random generation.
            If None, uses true randomness. Defaults to None.
        overwrite (bool, optional): Whether to overwrite existing file. Defaults to False.
        delimiter (str, optional): Field delimiter character for CSV output. Defaults to ",".
        quotechar (str, optional): Quote character for CSV fields. Defaults to '"'.

    Returns:
        None: Outputs CSV file to specified path.

    Raises:
        FileExistsError: If output file exists and overwrite=False.
        ValueError: If field configurations are invalid.

    Example:
        >>> config = [{
        ...     'name': 'age',
        ...     'type': 'int',
        ...     'min': 18,
        ...     'max': 65
        ... }]
        >>> generate_data("output.csv", num_samples=100, fields_config=config)
    """
    # 处理路径
    output_path = Path(output_path)

    # 检查文件是否存在
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"File {output_path} already exists. Set overwrite=True to overwrite."
        )

    # 验证字段配置
    if not fields_config:
        raise ValueError("fields_config must be provided and cannot be an empty list")

    # 检查name和type字段是否正确
    for config in fields_config:
        if "name" not in config:
            raise ValueError("Each field configuration must contain a 'name' key")
        if "type" not in config:
            raise ValueError(f"Field '{config['name']}' must contain a 'type' key")
        if config["type"] not in ("int", "float", "string", "date", "bool", "choice"):
            raise ValueError(
                f"Invalid type '{config['type']}' for field '{config['name']}'"
            )

    # 设置随机种子，未设置则无法复现结果
    if random_seed is not None:
        random.seed(random_seed)

    # 生成模拟数据
    data = []
    field_names = [field["name"] for field in fields_config]

    for _ in range(num_samples):
        row = {}
        for config in fields_config:
            field_name = config["name"]
            data_type = config["type"]
            if data_type == "int" or data_type == "float":
                min_val = config.get("min", 0)
                max_val = config.get("max", 100)
                scale_type = config.get("scale", "linear")
                base = config.get("base", 10)
                if scale_type == "log":
                    if min_val <= 0:
                        raise ValueError("对数分布的最小值必须大于0")
                    log_min = math.log(min_val, base)
                    log_max = math.log(max_val, base)
                    value = base ** random.uniform(log_min, log_max)
                elif scale_type == "linear":
                    value = random.uniform(min_val, max_val)
                else:
                    pass
                if data_type == "int":
                    row[field_name] = int(value)
                else:
                    decimals = config.get("decimals", 2)
                    row[field_name] = round(value, decimals)
            elif data_type == "string":
                length = config.get("length", 8)
                charset = config.get("charset", string.ascii_letters)
                prefix = config.get("prefix", "")
                suffix = config.get("suffix", "")
                random_part = "".join(random.choices(charset, k=length))
                row[field_name] = f"{prefix}{random_part}{suffix}"
            elif data_type == "date":
                start_date = config.get("start_date", "2020-01-01")
                end_date = config.get("end_date", "2023-12-31")
                date_format = config.get("format", "%Y-%m-%d")

                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")

                delta = end_date - start_date
                random_days = random.randint(0, delta.days)
                random_date = start_date + timedelta(days=random_days)
                row[field_name] = random_date.strftime(date_format)
            elif data_type == "bool":
                row[field_name] = random.choice([True, False])
            elif data_type == "choice":
                choices = config.get("choices", ["A", "B", "C"])
                weights = config.get("weights", None)
                row[field_name] = random.choices(choices, weights=weights, k=1)[0]

        data.append(row)

    # 写入CSV文件
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=field_names, delimiter=delimiter, quotechar=quotechar
        )
        writer.writeheader()
        writer.writerows(data)

    print(
        f"Successfully generated {num_samples} sample records to {Path(output_path).resolve()}"
    )
