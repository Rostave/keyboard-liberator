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
  <h4>以意想不到的方式解放你的控制器，實現新穎流暢的遊戲體驗</h4>
  <br />
</div>


![main](Doc/imgs/1.png)


## 簡介

Controller Liberator 是一個基於手勢的遊戲控制器，它使用電腦視覺和姿態檢測技術將你的身體動作轉換為遊戲控制。透過利用 MediaPipe 的姿態估計，這個應用程式允許你透過攝影機捕獲的手勢和身體姿勢來控制賽車遊戲（或其他相容遊戲）。

該系統提供即時視覺回饋，帶有透明疊加視窗，顯示你檢測到的手部位置和當前控制狀態（轉向、油門、剎車）。它的設計理念是有趣、易用，並且可以跨多個平台工作。


<p align="right">(<a href="#readme-top">返回頂部</a>)</p>


## 功能特性

- **即時姿態檢測**：使用 MediaPipe 高精度追蹤 33 個身體關鍵點
- **手勢到控制映射**：將手部位置轉換為遊戲控制（轉向、油門、剎車）
- **跨平台支援**：
  - **Windows**：透過 vgamepad 實現虛擬手把（XBOX 控制器模擬）
  - **macOS/Linux**：透過 pynput 實現鍵盤控制（WASD 鍵）
- **視覺回饋**：帶即時 UI 指示器的透明疊加視窗
  - 顯示轉向角度的動畫方向盤
  - 油門和剎車指示器
  - 手部位置追蹤
- **可自訂預設**：儲存和載入不同的控制配置
- **校準模式**：按 'K' 鍵切換以微調手部檢測範圍
- **可縮放 UI**：可調節視窗大小（預設 30% 縮放以實現非侵入式疊加）
- **抗鋸齒圖形**：使用 pygame 的 gfxdraw 實現平滑渲染
- **效能優化**：高效的影格處理和可配置的 FPS


<p align="right">(<a href="#readme-top">返回頂部</a>)</p>

## 平台特定說明

### Windows
- 透過 vgamepad 使用虛擬 XBOX 控制器模擬
- 安裝前需要在 requirements.txt 中取消註解 `vgamepad`
- 與支援 XBOX 控制器的遊戲相容性最佳
- TKParam 函式庫提供互動式校準控制

### macOS
- 使用鍵盤控制（WASD 鍵：A=左轉，D=右轉，W=油門，S=剎車）
- 除標準依賴外無需額外設定
- 由於 macOS 執行緒限制，TKParam GUI 被停用
- 使用 `Presets/` 目錄中的預設檔案進行校準調整

### Linux
- 使用鍵盤控制（WASD 鍵）
- 需要 pynput 依賴
- 設定方式與 macOS 類似


<p align="right">(<a href="#readme-top">返回頂部</a>)</p>


<!-- GETTING STARTED -->
## 開始使用

### 前置要求

1. **Python 3.8+**（已在 Python 3.11.6 上測試）
2. **攝影機** - 內建或外接 USB 攝影機
3. **平台特定要求**：
   - **Windows**：在 `requirements.txt` 中取消註解 `vgamepad` 以啟用手把模擬
   - **macOS/Linux**：預設配置使用鍵盤控制（無需額外步驟）

### 安裝

1. 複製儲存庫：
   ```sh
   git clone https://github.com/Rostave/controller-liberator.git
   cd controller-liberator
   ```

2. 安裝依賴：
   
   **macOS/Linux 使用者：**
   ```sh
   pip install -r requirements.txt
   ```
   
   **Windows 使用者（虛擬手把支援）：**
   - 首先，在 `requirements.txt` 中取消註解 `vgamepad` 行
   - 然後安裝：
   ```sh
   pip install -r requirements.txt
   ```

3. （可選）在 `sysconfig.ini` 中配置設定：
   - 調整攝影機解析度、FPS 顯示、MediaPipe 設定
   - 更改預設預設或校準鍵

### 執行

```sh
python main.py
```

### 控制方式

- **K 鍵**：切換校準模式（僅限 Windows 配合 TKParam）
- **手勢操作**：
  - **油門**：增加兩個拳頭之間的間距，讓兩個拳頭都落在紅色區域內。你的手越靠近紅色外圈，加速越快。
  - **剎車**：減少兩個拳頭之間的間距，讓兩個拳頭都落在藍色區域內。你的手越靠近藍色內圈，減速越快。
  - **轉向**：轉動雙手，就像握著方向盤一樣
- 按關閉視窗按鈕退出程式，系統會詢問是否儲存當前預設。

### 範例遊戲
- **遊戲連結**：在此下載 Mac 和 Windows 版範例遊戲：https://flamberge-backtrace.itch.io/simple-car-simulator


### 故障排除

**攝影機未檢測到：**
- 檢查系統設定中的攝影機權限
- 嘗試在程式碼中更改攝影機索引（預設為 0）

**Windows：遊戲對控制無回應：**
- 確保已安裝 vgamepad
- 檢查遊戲是否支援 XBOX 控制器

**macOS：按 'K' 鍵時程式當機：**
- 這是預期行為 - macOS 上停用了 TKParam GUI
- 使用 `Presets/` 目錄中的預設 JSON 檔案進行校準

**效能問題：**
- 在 `sysconfig.ini` 中降低攝影機解析度
- 降低 MediaPipe 模型複雜度（設定為 0 或 1）

<p align="right">(<a href="#readme-top">返回頂部</a>)</p>



<!-- CONTRIBUTING -->
## 貢獻者

<a href="https://github.com/Rostave/controller-liberator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Rostave/controller-liberator" alt="contrib.rocks image" />
</a>

每位組員對專案的貢獻均等。

<p align="right">(<a href="#readme-top">返回頂部</a>)</p>



<!-- LICENSE -->
## 授權

目前未授權。

<p align="right">(<a href="#readme-top">返回頂部</a>)</p>



<!-- CONTACT -->
## 聯絡方式

bitCirno - [@bitCirno](https://b23.tv/3oXghzO) (Bilibili) - 1637131272@qq.com

<!-- 可以留下自己的其他平台联系方式 -->

[BAO-Hongzhen](https://drive.google.com/file/d/1aBJJ7bUIs24Dfr7240TMOpYMR8GOCc6r/view?usp=sharing) - [@wQd](https://b23.tv/KLyimBu) (Bilibili) - 15874816801@163.com

<p align="right">(<a href="#readme-top">返回頂部</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## 致謝

* [Pygame](https://www.pygame.org/news)
* [tkparam](https://github.com/Rostave/tkparam)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">返回頂部</a>)</p>



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
