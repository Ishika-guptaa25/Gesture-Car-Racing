# 🚗 Hand Gesture Car Racing Game

An interactive racing game controlled entirely by hand gestures using computer vision and AI! Built with Python, OpenCV, MediaPipe, and Pygame.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎮 Features

- 🤚 **Hand Gesture Controls** - No keyboard or mouse needed!
- 🎯 **Real-time AI Tracking** - Powered by MediaPipe
- 🏎️ **Smooth Physics** - Realistic acceleration and steering
- 🚧 **Dynamic Obstacles** - Avoid other cars on the highway
- 📊 **Score System** - Compete for high scores
- 📷 **Live Camera Feed** - See your hand movements
- 🎨 **Colorful Graphics** - Beautiful 2D rendering
- ⚡ **60 FPS Gameplay** - Smooth and responsive

## 🕹️ Gesture Controls

| Gesture | Action |
|---------|--------|
| **Tilt hand LEFT** ← | Steer left |
| **Tilt hand RIGHT** → | Steer right |
| **Palm FORWARD** 🖐️ | Accelerate |
| **No hand** | Slow down |

## 🖼️ Screenshots

```
┌─────────────────────────────────────┐
│  Score: 12,450      Lives: ❤️ ❤️ ❤️   │
│  Distance: 124.5m   Speed: 75%     │
├─────────────────────────────────────┤
│              |     🚗    |          │
│              |           |          │
│              |     🚗    |          │
│              |           |          │
│              |     YOU   |          │
│              └───────────┘          │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Webcam** connected
- **Git** installed (for cloning)
- **pip** package manager

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ishika-guptaa25/Gesture-Car-Racing.git
cd Gesture-Car-Racing
```

### 2. Create Virtual Environment 

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Game

```bash
python main.py
```

## 📁 Project Structure

```
gesture-car-racing/
├── main.py                 # Main entry point
├── game.py                 # Game logic and rendering
├── gesture_controller.py   # AI gesture detection
├── car.py                  # Player car class
├── obstacles.py            # Obstacle management
├── config.py               # Game configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
```

## 🎯 How to Play

1. **Start the game** - Run `python main.py`
2. **Position yourself** - Sit 2-3 feet from the camera
3. **Show your hand** - Raise your hand in front of the camera
4. **Control the car**:
   - Tilt your hand left/right to steer
   - Push your palm forward to accelerate
5. **Avoid obstacles** - Don't crash into other cars!
6. **Score points** - The longer you survive, the higher your score

## ⌨️ Keyboard Controls

If camera is not available, use keyboard:

- **LEFT ARROW** - Steer left
- **RIGHT ARROW** - Steer right
- **UP ARROW** - Accelerate
- **SPACE** - Pause/Resume
- **C** - Toggle camera view
- **R** - Restart (when game over)
- **ESC** - Quit game

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Car settings
CAR_SPEED = 300
CAR_MAX_SPEED = 500

# Gesture thresholds
TILT_LEFT_THRESHOLD = -0.15
TILT_RIGHT_THRESHOLD = 0.15
PALM_FORWARD_THRESHOLD = 0.6
```

## 🐛 Troubleshooting

### Camera Not Working

```bash
# Check camera index
# Try changing CAMERA_INDEX in config.py
CAMERA_INDEX = 0  # Try 1, 2, etc.
```

### Poor Gesture Detection

- **Ensure good lighting**
- **Position hand clearly** in camera view
- **Adjust thresholds** in `config.py`
- **Keep background simple**

### Low FPS

- **Close other applications**
- **Lower resolution** in `config.py`
- **Update graphics drivers**

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 To-Do List

- [ ] Add power-ups (shields, speed boost)
- [ ] Implement multiplayer mode
- [ ] Add sound effects and music
- [ ] Create different tracks/environments
- [ ] Add difficulty levels
- [ ] Implement high score leaderboard
- [ ] Add car customization
- [ ] Create mobile version

## 🎓 Learning Resources

This project uses:

- **[MediaPipe](https://mediapipe.dev/)** - Hand tracking
- **[OpenCV](https://opencv.org/)** - Computer vision
- **[Pygame](https://www.pygame.org/)** - Game development
- **[NumPy](https://numpy.org/)** - Numerical computing

## 🙏 Acknowledgments

- MediaPipe team for amazing hand tracking
- Pygame community for game development resources
- OpenCV for computer vision tools
- Everyone who contributed to this project


