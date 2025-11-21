[//]: # (Reference: https://github.com/Rostave/Best-README-Template by othneildrew)
<a id="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]

<div align="center">

### [English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Controller Liberator</h1>
  <h4>以意想不到的方式解放你的控制器，实现新颖流畅的游戏体验</h4>
  <br />
</div>


![main](Doc/imgs/1.png)


## 简介

Controller Liberator 是一个基于手势的游戏控制器，它使用计算机视觉和姿态检测技术将你的身体动作转换为游戏控制。通过利用 MediaPipe 的姿态估计，这个应用程序允许你通过摄像头捕获的手势和身体姿势来控制赛车游戏（或其他兼容游戏）。

该系统提供实时视觉反馈，带有透明叠加窗口，显示你检测到的手部位置和当前控制状态（转向、油门、刹车）。它的设计理念是有趣、易用，并且可以跨多个平台工作。


<p align="right">(<a href="#readme-top">返回顶部</a>)</p>


## 功能特性

- **实时姿态检测**：使用 MediaPipe 高精度追踪 33 个身体关键点
- **手势到控制映射**：将手部位置转换为游戏控制（转向、油门、刹车）
- **跨平台支持**：
  - **Windows**：通过 vgamepad 实现虚拟手柄（XBOX 控制器模拟）
  - **macOS/Linux**：通过 pynput 实现键盘控制（WASD 键）
- **视觉反馈**：带实时 UI 指示器的透明叠加窗口
  - 显示转向角度的动画方向盘
  - 油门和刹车指示器
  - 手部位置追踪
- **可自定义预设**：保存和加载不同的控制配置
- **校准模式**：按 'K' 键切换以微调手部检测范围
- **可缩放 UI**：可调节窗口大小（默认 30% 缩放以实现非侵入式叠加）
- **抗锯齿图形**：使用 pygame 的 gfxdraw 实现平滑渲染
- **性能优化**：高效的帧处理和可配置的 FPS


<p align="right">(<a href="#readme-top">返回顶部</a>)</p>

## 平台特定说明

### Windows
- 通过 vgamepad 使用虚拟 XBOX 控制器模拟
- 安装前需要在 requirements.txt 中取消注释 `vgamepad`
- 与支持 XBOX 控制器的游戏兼容性最佳
- TKParam 库提供交互式校准控制

### macOS
- 使用键盘控制（WASD 键：A=左转，D=右转，W=油门，S=刹车）
- 除标准依赖外无需额外设置
- 由于 macOS 线程限制，TKParam GUI 被禁用
- 使用 `Presets/` 目录中的预设文件进行校准调整

### Linux
- 使用键盘控制（WASD 键）
- 需要 pynput 依赖
- 设置方式与 macOS 类似


<p align="right">(<a href="#readme-top">返回顶部</a>)</p>


<!-- GETTING STARTED -->
## 开始使用

### 前置要求

1. **Python 3.8+**（已在 Python 3.11.6 上测试）
2. **摄像头** - 内置或外接 USB 摄像头
3. **平台特定要求**：
   - **Windows**：在 `requirements.txt` 中取消注释 `vgamepad` 以启用手柄模拟
   - **macOS/Linux**：默认配置使用键盘控制（无需额外步骤）

### 安装

1. 克隆仓库：
   ```sh
   git clone https://github.com/Rostave/controller-liberator.git
   cd controller-liberator
   ```

2. 安装依赖：
   
   **macOS/Linux 用户：**
   ```sh
   pip install -r requirements.txt
   ```
   
   **Windows 用户（虚拟手柄支持）：**
   - 首先，在 `requirements.txt` 中取消注释 `vgamepad` 行
   - 然后安装：
   ```sh
   pip install -r requirements.txt
   ```

3. （可选）在 `sysconfig.ini` 中配置设置：
   - 调整摄像头分辨率、FPS 显示、MediaPipe 设置
   - 更改默认预设或校准键

### 运行

```sh
python main.py
```

### 控制方式

- **K 键**：切换校准模式（仅限 Windows 配合 TKParam）
- **手势操作**：
  - **油门**：增加两个拳头之间的间距，让两个拳头都落在红色区域内。你的手越靠近红色外圈，加速越快。
  - **刹车**：减少两个拳头之间的间距，让两个拳头都落在蓝色区域内。你的手越靠近蓝色内圈，减速越快。
  - **转向**：转动双手，就像握着方向盘一样
- 按关闭窗口按钮退出程序，系统会询问是否保存当前预设。

### 示例游戏
- **游戏链接**：在此下载 Mac 和 Windows 版示例游戏：https://flamberge-backtrace.itch.io/simple-car-simulator


### 故障排除

**摄像头未检测到：**
- 检查系统设置中的摄像头权限
- 尝试在代码中更改摄像头索引（默认为 0）

**Windows：游戏对控制无响应：**
- 确保已安装 vgamepad
- 检查游戏是否支持 XBOX 控制器

**macOS：按 'K' 键时程序崩溃：**
- 这是预期行为 - macOS 上禁用了 TKParam GUI
- 使用 `Presets/` 目录中的预设 JSON 文件进行校准

**性能问题：**
- 在 `sysconfig.ini` 中降低摄像头分辨率
- 降低 MediaPipe 模型复杂度（设置为 0 或 1）

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>



<!-- CONTRIBUTING -->
## 贡献者

<a href="https://github.com/Rostave/controller-liberator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Rostave/controller-liberator" alt="contrib.rocks image" />
</a>

每位组员对项目的贡献均等。

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>



<!-- LICENSE -->
## 许可证

目前未授权。

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>



<!-- CONTACT -->
## 联系方式

bitCirno - [@bitCirno](https://b23.tv/3oXghzO) (Bilibili) - 1637131272@qq.com

<!-- 可以留下自己的其他平台联系方式 -->

[BAO-Hongzhen](https://drive.google.com/file/d/1aBJJ7bUIs24Dfr7240TMOpYMR8GOCc6r/view?usp=sharing) - [@wQd](https://b23.tv/KLyimBu) (Bilibili) - 15874816801@163.com

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## 致谢

* [Pygame](https://www.pygame.org/news)
* [tkparam](https://github.com/Rostave/tkparam)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Rostave/controller-liberator.svg?style=for-the-badge
[contributors-url]: https://github.com/Rostave/controller-liberator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Rostave/controller-liberator.svg?style=for-the-badge
[forks-url]: https://github.com/Rostave/controller-liberator/network/members
[stars-shield]: https://img.shields.io/github/stars/Rostave/controller-liberator.svg?style=for-the-badge
[stars-url]: https://github.com/Rostave/controller-liberator/stargazers
[issues-shield]: https://img.shields.io/github/issues/Rostave/controller-liberator.svg?style=for-the-badge
[issues-url]: https://github.com/Rostave/controller-liberator/issues
[license-shield]: https://img.shields.io/github/license/Rostave/controller-liberator.svg?style=for-the-badge
[license-url]: https://github.com/Rostave/controller-liberator/blob/master/LICENSE.txt
