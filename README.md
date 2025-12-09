# QuickPlot

## 项目说明

通过 numpy，matplotlib 和 seaborn 等数据处理和绘图包，复现一些没提供原始 Python 代码的顶刊图表。

## 目录说明

plot 文件夹中放置的是绘图的主要代码；utils 文件夹中放置的是绘图的工具函数。

## 错误解决

如果遇到以下类似错误（没有可忽略），即无法识别自定义的 utils 模块时，

ModuleNotFoundError: No module named 'utils'

Parent module 'utils' not loaded, cannot perform relative import

可以尝试以下解决方法：

1.Pycharm（演示版本为 2025.02）

在 Pycharm 中，找到 utils 文件夹，右键选择【Make Directory as】|【Source Root】，之后重启 Pycharm 即可。

![image-20251209220547684](https://cdn.jsdelivr.net/gh/zbhgis/BlogImg@main/blog/202512092205789.png)

![image-20251209220925063](https://cdn.jsdelivr.net/gh/zbhgis/BlogImg@main/blog/202512092209104.png)

2.Visual Studio Code（演示版本为 1.102.3）

在 VS Code 中，在仓库目录下新建文件夹，命名为 .vscode

在 .vscode 文件夹下，新建文件，命名为 settings.json

在其中输入以下内容后保存即可，之后重启 Python 解释器或者 VS Code

![image-20251209222113287](https://cdn.jsdelivr.net/gh/zbhgis/BlogImg@main/blog/202512092221329.png)

```python
{
 "terminal.integrated.env.windows": {
  "PYTHONPATH": "${workspaceFolder}"
 }
}
```
