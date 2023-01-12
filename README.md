![LOGO](res/image/LOGO_light.png)

# pyGobang

English | [简体中文](./README_CN.md)

A python based gobang game.

## Status

The game has currently been released version v0.2.1, currently to basically complete the functional goals.

If you find a bug, feel free to write issues and let me know ~ 😉

The game uses pygame as the graphics engine and uses SQLite to record historical games.

The human-computer part of the game is modified from @Xshellye 's open source project [GoBang-python-homework](https://github.com/Xshellye/GoBang-python-homework).

The game font is the open source font [Sarasa-Mono-SC-Nerd](https://github.com/laishulu/Sarasa-Mono-SC-Nerd).

The game demo has been released on [bilibili](https://www.bilibili.com/video/BV1iL4y1N79m).

*A big thank you to my friends @Charholer and @Vokain for the music as well as the sound support.*

## Installation

Download the (soon to be released) release version, or clone the project locally and run it, as described in the [Configuring the Environment section](#1-configuring-the-environment) below.

## Build a release

**Notice: Currently the game is only written to build scripts for the windows environment!**

### 1 Configuring the environment

Note: Make sure that Miniconda or Anaconda is installed on your computer.

Execute the following code in sequence:

```sh
git clone https://github.com/JesseSenior/pyGobang
cd pyGobang
conda env create -f environment.yml
conda activate pyGobang_env
```

Then you can enter the project development environment, if you execute `python pyGobang.py` to start the game body.

In addition, you can also configure the environment by executing the following code:

```sh
conda create -n "pyGobang_env" `
    python=3.10 nomkl black numpy `
    pillow pip scipy scikit-image sqlite `
    ordered-set pyinstaller `
    --no-default-packages -y

conda activate pyGobang_env
pip install pygame
```

### 2 Execute packing script (beta)

```sh
cd script
./build.ps1
```

Wait for the script to finish and you will get game's binary named "pyGobang.exe" in the root directory of the project.
