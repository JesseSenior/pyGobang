![LOGO](res/image/LOGO_light.png)

# pyGobang

English | [简体中文](./README_CN.md)

A python based gobang game.

## Status

The game has currently been released version v0.1.0, currently to basically complete the functional goals, but still **may exist huge amount of bugs**. :(

If you find bugs, welcome to point out ~~~

The game uses pygame as the graphics engine and uses sqlite to record historical games.

The game currently uses Monte Carlo Search Trees (MCTS) to implement the human-computer part, and will be optimized opportunistically afterwards.

The game font is the open source font [Sarasa-Mono-SC-Nerd](https://github.com/laishulu/Sarasa-Mono-SC-Nerd).

The game demo has been released on [bilibili](https://www.bilibili.com/video/BV1iL4y1N79m).

*A big thank you to my friends @Charholer and @Vokain for the music as well as the sound support.*

## How to Play

Download the (soon to be released) release version, or clone the project locally and run it, as described in the [Configuring the Environment section](#1-configuring-the-environment) below.

## How to Pack

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

### 2 Execute packing script (beta)

```sh
cd script
./build.ps1
```

Wait for the script to finish and you will get the game executable in the "dist" directory of the script.
