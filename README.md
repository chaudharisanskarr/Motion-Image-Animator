# Motion Image Animator

This project animates static images by applying natural effects (like wind) to specific visual elements such as boats, clouds, trees, and water surfaces. The animations are based on the paper [Animating Pictures with Stochastic Motion Textures](http://grail.cs.washington.edu/projects/StochasticMotionTextures/) by Chuang et al.

## 🎯 Objective

Enhance real-world or artistic pictures (e.g., Monet-style paintings) by simulating realistic motion through segmentation and transformation techniques.

## 📁 Project Structure

Motion Image Animator/
├── shaders/ # GLSL shader files for visual effects
├── .vscode/ # VSCode settings
├── main.py # Main Python script to run the project
├── imgui.ini # GUI configuration
├── *.png, *.jpg, *.gif # Input images and textures
├── wave.wav # Optional sound file
└── README.md # This file

## 🖼️ Sample Output

| Original Image | Animated Result |
|----------------|-----------------|
| `boatMonet.jpg` | `boatCG.gif` |
| `bridgeMonet.jpg` | `bridgeCG.gif` |

## 🛠️ Dependencies

Make sure to install the following:

- [OpenCV](https://opencv.org/)
- [GLFW](https://www.glfw.org/)
- Python packages: `numpy`, `opencv-python`, `PyOpenGL`, `imgui`, `pygame`

Install via pip:
```sh
pip install numpy opencv-python PyOpenGL imgui pygame
🚀 How to Run
Basic Execution
sh
Copy
Edit
python main.py
Make sure your selected assets (e.g., background2.png, boat2.png, tree2.png, etc.) are placed in the root folder.

Optional: Customize Input
Update the paths in main.py if you want to use different images or effects. You can add your own .png or .jpg files to simulate new motion textures.

## 🧭 GUI Features
Cloud / Boat / Tree / Water Buttons: Select areas for segmentation.

Point Selectors: Define transformation points for tree or boat.

Wind Slider: Adjust the wind speed to influence motion.

Show Button: Apply transformations and view animated image.

Segmentation Controls
s – Segment the marked region.

r – Reset selection.

Esc – Exit popup window.

## 📄 Report
For detailed documentation, refer to the included file CG CP.docx.#
