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



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Controller Liberator</h1>
  <h4>Liberate your controller in unexpected ways and achieve a novel and smooth gaming experience</h4>
  <br />
</div>


![main](Doc/imgs/1.png)


## Introduction

Controller Liberator is a gesture-based game controller that transforms your body movements into game controls using computer vision and pose detection. By leveraging MediaPipe's pose estimation, this application allows you to control racing games (or other compatible games) through hand gestures and body postures captured by your webcam.

The system provides real-time visual feedback with a transparent overlay window, showing your detected hand positions and current control states (steering, throttle, brake). It's designed to be fun, accessible, and works across multiple platforms.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Features

- **Real-time Pose Detection**: Uses MediaPipe to track 33 body landmarks with high accuracy
- **Gesture-to-Control Mapping**: Converts hand positions into game controls (steering, throttle, brake)
- **Cross-Platform Support**: 
  - **Windows**: Virtual gamepad via vgamepad (XBOX controller emulation)
  - **macOS/Linux**: Keyboard control via pynput (WASD keys)
- **Visual Feedback**: Transparent overlay window with real-time UI indicators
  - Animated steering wheel showing turn angle
  - Throttle and brake indicators
  - Hand position tracking
- **Customizable Presets**: Save and load different control configurations
- **Calibration Mode**: Toggle with 'K' key to fine-tune hand detection ranges
- **Scalable UI**: Adjustable window size (default 30% scale for non-intrusive overlay)
- **Anti-aliased Graphics**: Smooth rendering using pygame's gfxdraw
- **Performance Optimized**: Efficient frame processing with configurable FPS


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Platform-Specific Notes

### Windows
- Uses virtual XBOX controller emulation via vgamepad
- Requires uncommenting `vgamepad` in requirements.txt before installation
- Best compatibility with games that support XBOX controllers
- TKParam library provides interactive calibration controls

### macOS
- Uses keyboard control (WASD keys: A=left, D=right, W=throttle, S=brake)
- No additional setup required beyond standard dependencies
- TKParam GUI is disabled due to macOS threading limitations
- Use preset files in `Presets/` directory for calibration adjustments

### Linux
- Uses keyboard control (WASD keys)
- Requires pynput dependency
- Similar to macOS setup


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. **Python 3.8+** (tested with Python 3.11.6)
2. **Webcam** - Built-in or external USB camera
3. **Platform-specific requirements**:
   - **Windows**: Uncomment `vgamepad` in `requirements.txt` for gamepad emulation
   - **macOS/Linux**: Default configuration uses keyboard control (no extra steps)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Rostave/controller-liberator.git
   cd controller-liberator
   ```

2. Install dependencies:
   
   **For macOS/Linux users:**
   ```sh
   pip install -r requirements.txt
   ```
   
   **For Windows users (virtual gamepad support):**
   - First, uncomment the `vgamepad` line in `requirements.txt`
   - Then install:
   ```sh
   pip install -r requirements.txt
   ```

3. (Optional) Configure settings in `sysconfig.ini`:
   - Adjust camera resolution, FPS display, MediaPipe settings
   - Change default preset or calibration key

### Running

```sh
python main.py
```

### Controls

- **K key**: Toggle calibration mode (Windows only with TKParam)
- **ESC**: Exit application
- **Hand gestures**:
  - Raise both hands above shoulders: Throttle
  - Lower both hands below hips: Brake
  - Move hands left/right: Steering

### Troubleshooting

**Camera not detected:**
- Check camera permissions in system settings
- Try changing camera index in code (default is 0)

**Windows: Game not responding to controls:**
- Ensure vgamepad is installed
- Check if game supports XBOX controllers

**macOS: Program crashes on 'K' key:**
- This is expected - TKParam GUI is disabled on macOS
- Use preset JSON files in `Presets/` directory for calibration

**Performance issues:**
- Lower camera resolution in `sysconfig.ini`
- Reduce MediaPipe model complexity (set to 0 or 1)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributors

<a href="https://github.com/Rostave/controller-liberator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Rostave/controller-liberator" alt="contrib.rocks image" />
</a>

Every group member contribute equally to the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Unlicensed currently.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

bitCirno - [@bitCirno](https://b23.tv/3oXghzO) (Bilibili) - 1637131272@qq.com

<!-- 可以留下自己的其他平台联系方式 -->

[BAO-Hongzhen](https://drive.google.com/file/d/1aBJJ7bUIs24Dfr7240TMOpYMR8GOCc6r/view?usp=sharing) - [@wQd](https://b23.tv/KLyimBu) (Bilibili) - 15874816801@163.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Pygame](https://www.pygame.org/news)
* [tkparam](https://github.com/Rostave/tkparam)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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


