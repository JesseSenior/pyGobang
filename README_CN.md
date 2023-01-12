![LOGO](res/image/LOGO_light.png)

# pyGobang

[English](./README.md) | 简体中文

一款基于python的五子棋小游戏。

## 状态

游戏当前已发布版本v0.2.1，目前已基本完成功能性目标。

如果发现BUG，欢迎拿issue砸我~😉

游戏使用pygame作为图形引擎，利用SQLite记录历史棋局。

游戏人机对战部分修改自@Xshellye的开源项目[GoBang-python-homework](https://github.com/Xshellye/GoBang-python-homework)。

游戏字体为开源字体[Sarasa-Mono-SC-Nerd](https://github.com/laishulu/Sarasa-Mono-SC-Nerd)。

游戏demo已发布于[bilibili](https://www.bilibili.com/video/BV1iL4y1N79m)。

*衷心感谢我的朋友@Charholer和@Vokain提供的音乐以及音效支持。*

## 如何游玩

下载（即将发布的）release版本，或者clone本项目至本地后运行，具体参看下文[配置环境](#1-配置环境)部分。

## 如何构建

**注意：目前游戏仅编写了windows环境下构建脚本！**

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

除此之外，你也可以通过执行以下代码来配置环境：

```sh
conda create -n "pyGobang_env" `
    python=3.10 nomkl black numpy `
    pillow pip scipy scikit-image sqlite `
    ordered-set pyinstaller `
    --no-default-packages -y

conda activate pyGobang_env
pip install pygame
```

### 2 执行打包脚本

```sh
cd script
./build_win.ps1
```

等待脚本结束后，即可在项目根目录下得到游戏可执行文件（通常命名为“pyGobang.exe”）。
