import utils

# 配置
scatter_config = [
    {
        "name": "snowmelt",
        "type": "float",
        "min": 0.05,
        "max": 60,
        "scale": "log",
        "decimals": 2,
    },
    {
        "name": "area total",
        "type": "int",
        "min": 1,
        "max": 800,
        "scale": "log",
    },
    {
        "name": "type",
        "type": "choice",
        "choices": ["EAIS", "AP", "WAIS"],
        "weights": [1, 1, 1],
    },
    {
        "name": "time",
        "type": "choice",
        "choices": ["November", "December", "January", "February"],
        "weights": [1, 1, 1, 1],
    },
]

csv_path = "scatter_data.csv"
# 创建散点图数据
utils.generate_data(
    output_path=csv_path,
    num_samples=120,
    fields_config=scatter_config,
    random_seed=13,
    overwrite=True,
)
