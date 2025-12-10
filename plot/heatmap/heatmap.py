"""
Author: https://github.com/zbhgis
Paper source: https://www.nature.com/articles/s41558-025-02363-5
Paper Figure source: https://www.nature.com/articles/s41558-025-02363-5/figures/3
Last Modified: 2025-12-03
Data: The data used in the code is generated randomly
"""

import numpy as np
import matplotlib.pyplot as plt
import utils


def create_heatmap(
    ax,
    vmin,
    vmax,
    heatmap_data,
    heatmap_cmap,
    x_tick_labels,
    y_tick_labels,
    x_tick_labels_tag=True,
    x_tick_length=0.026,
):
    # 绘制热力图
    im = ax.imshow(heatmap_data, cmap=heatmap_cmap, vmin=vmin, vmax=vmax)

    # 长宽比设置,调整单元格大小
    ax.set_aspect(aspect=1.2)

    # 添加白色间隔线
    # 横线设置宽一些，用于分割不同类型
    for i in range(len(y_tick_labels) + 1):
        ax.axhline(i - 0.5, color="white", lw=10)
    # 竖线设置窄一些
    for j in range(len(x_tick_labels) + 1):
        ax.axvline(j - 0.5, color="white", lw=2)

    # 设置x轴
    ax.set_xticks(np.arange(len(x_tick_labels)))
    # 如果需要绘制x轴时间刻度标签
    if x_tick_labels_tag:
        ax.set_xticklabels(
            labels=x_tick_labels,
            rotation=45,
            horizontalalignment="right",
            rotation_mode="anchor",
        )
    else:
        ax.set_xticklabels(labels="")
    # 添加新的x轴刻度线
    utils.add_ticks(
        ax,
        axis="x",
        positions=ax.get_xticks(),
        ymin=0.002,
        ymax=x_tick_length,
    )

    # 设置y轴
    ax.set_yticks(np.arange(len(y_tick_labels)))
    ax.set_yticklabels(y_tick_labels)
    ax.tick_params(axis="y", which="both", length=0)

    # 移除之前的网格线
    ax.grid(False)

    return im


if __name__ == "__main__":
    # 统一绘图样式
    plt.rcdefaults()
    plt.rcParams.update(
        {
            "font.family": "Arial",  # 字体
            "axes.titlesize": 16,  # 子图标题大小
            "axes.labelsize": 16,  # 坐标轴标签大小
            "xtick.labelsize": 16,  # x轴刻度标签大小
            "ytick.labelsize": 16,  # y轴刻度标签大小
            "legend.fontsize": 12,  # 图例字体大小
            "axes.linewidth": 1,  # 坐标轴线宽
            "lines.linewidth": 1,  # 线宽
            "legend.handlelength": 0.6,  # 图例长度
            "legend.handleheight": 0.6,  # 图例高度
            "legend.handletextpad": 0.3,  # 图例与图例文字距离
        }
    )

    # 生成模拟数据
    x_tick_labels = []
    for i in range(15):
        category = f"{2006 + i}/{str(2006 + i + 1)[-2:]}"
        if i == 12:
            category += "*"
        x_tick_labels.append(category)
    y_tick_labels_list = [
        ["EAIS total"],
        ["Rennick", "Shackleton", "Amery", "Baudouin", "Nivlisen"],
        ["AP total"],
        ["Wilkins", "Bach", "George VI"],
        ["WAIS total"],
    ]
    heatmap_data_list = []
    for i in range(len(y_tick_labels_list)):
        np.random.seed(13 + i)
        heatmap_data = np.random.uniform(
            low=-3, high=3, size=(len(y_tick_labels_list[i]), len(x_tick_labels))
        )
        heatmap_data_list.append(heatmap_data)

    # 设置色带
    cmap = "RdBu_r"

    # 因为刻度线长度是按照比例的，所以设置不同的刻度线长度
    x_tick_length = [0.1, 0.026, 0.1, 0.05, 0.1]

    # 绘制子图
    fig, ax_list = utils.add_subplots(
        tw=10,
        th=14,
        nrows=12,
        ncols=1,
        gs_loc=[[0, 0], [(1, 6), 0], [6, 0], [(7, 10), 0], [(10, 12), 0]],
        ax_offsets=[[0, -0.05], [0, 0], [0, -0.03], [0, 0], [0, 0]],
        hspace=0.3,
        text_type="a",
        text_step=2,
        text_offsets=[[-0.06, 1], [0, 1], [-0.06, 1], [0, 1], [-0.06, 1]],
    )

    # 第一幅和第三幅子图不绘制x轴刻度标签
    for i in range(len(ax_list)):
        if i == 0 or i == 2:
            tag = False
        else:
            tag = True
        im = create_heatmap(
            ax_list[i],
            vmin=-3,
            vmax=3,
            heatmap_data=heatmap_data_list[i],
            heatmap_cmap=cmap,
            x_tick_labels=x_tick_labels,
            y_tick_labels=y_tick_labels_list[i],
            x_tick_labels_tag=tag,
            x_tick_length=x_tick_length[i],
        )
        # 第五幅子图添加最下方的x轴标签和横线
        if i == 4:
            ax_list[i].text(
                0.45,
                -1.65,
                "Years",
                ha="center",
                va="center",
                transform=ax_list[i].transAxes,
                fontsize=16,
            )
            ax_pos = ax_list[i].get_position()
            utils.add_line(
                ax=ax_list[i],
                x=[ax_pos.x0 - 0.06, ax_pos.x0 + ax_pos.width],
                y=[ax_pos.y0 - 0.06, ax_pos.y0 - 0.06],
                transform="figure",
                clip_on=False,
            )
        # 添加子图外部上方横线
        if i % 2 == 0:
            ax_pos = ax_list[i].get_position()
            utils.add_line(
                ax=ax_list[i],
                x=[ax_pos.x0 - 0.06, ax_pos.x0 + ax_pos.width],
                y=[ax_pos.y1 + 0.02, ax_pos.y1 + 0.02],
                transform="figure",
                clip_on=False,
            )

    # 添加colorbar，并添加标签
    cax = fig.add_axes([0.92, 0.09, 0.04, 0.75])  # [left, bottom, width, height]
    cbar = fig.colorbar(im, cax=cax, label="Total meltwater area Z-score")
    cbar.set_label(
        "Total meltwater area Z-score", rotation=-90, labelpad=20, fontsize=18
    )
    cbar.ax.tick_params(direction="in", which="both")
    # 添加colorbar内部说明文字
    cbar.ax.text(
        0.5,
        0.35,
        "\n".join("BELOW AVERAGE"),
        transform=cbar.ax.transAxes,
        ha="center",
        va="top",
        color="white",
        fontsize=18,
    )
    cbar.ax.text(
        0.5,
        0.98,
        "\n".join("ABOVE AVERAGE"),
        transform=cbar.ax.transAxes,
        ha="center",
        va="top",
        color="white",
        fontsize=18,
    )

    # 导出为jpg文件，默认在当前路径下
    utils.export_fig()
    # 导出为指定路径下的指定文件名的tiff文件，dpi为500
    # utils.export_fig(
    #     formats="tiff", output_path=r"C:\Users\dell\Desktop\test.tiff", dpi=500
    # )

    # # 直接用plt.show()会导致比例失常，所以得看最终导出的图。
    # plt.show()
