![LOGO](res/image/LOGO_light.png)

# pyGobang

[English](./README.md) | 简体中文

一款基于python的五子棋小游戏。

## 状态

游戏当前仍处在开发中，因此**可能存在巨量BUG**。 :(

如果发现BUG，欢迎指出~~~

游戏使用pygame作为图形引擎，利用sqlite记录历史棋局。

游戏目前使用蒙特卡洛搜索树(MCTS)实现人机对战部分，之后会择机优化。

游戏字体为开源字体[Sarasa-Mono-SC-Nerd](https://github.com/laishulu/Sarasa-Mono-SC-Nerd)。

*衷心感谢我的朋友@Charholer和@Vokain提供的音乐以及音效支持。*

## 如何游玩

下载（即将发布的）release版本，或者clone本项目至本地后运行，具体参看下文[配置环境](#1-配置环境)部分。

## 如何打包

### 1 配置环境

注意：请确保电脑上安装有Miniconda或者Anaconda。

依次执行代码：

```sh
git clone https://github.com/JesseSenior/pyGobang
cd pyGobang
conda env create -f environment.yml
conda activate pyGobang_env
```

即可进入项目开发环境，此时若执行`python pyGobang.py`即可启动游戏主体。

### 2 执行打包脚本

```sh
cd script
./build.ps1
```

等待脚本结束后，即可在脚本"dist"目录下得到游戏可执行文件。
