# AI Hand Gesture Virtual Mouse

An advanced, contactless virtual mouse controller built using Python, OpenCV, and Google's MediaPipe. This project allows you to control your computer's cursor, perform clicks, scroll, and adjust volume entirely through hand gestures in real-time without needing any physical hardware.

## Features & Gesture Mapping

This project maps natural hand movements to system-level commands with high accuracy:

* ☝️ **Cursor Control:** Move the mouse pointer smoothly by pointing your **Index Finger** up.
* 🤏 **Left Click:** Perform a natural **Pinch gesture** (bringing the Index finger and Thumb tips together) to left-click.
* ✌️ **Right Click:** Display the **Peace Sign** (Index + Middle fingers up) to trigger a right-click.
* 🖐️ **Smart Scrolling:** Hold an **Open Palm** and slide your hand vertically up or down to scroll through webpages or documents.
* 👍/👎 **Volume Control:** Form a fist and point your **Thumb Up** to increase volume, or **Thumb Down** to decrease it.
* 📌 **Always-on-Top Camera:** The webcam feed stays pinned to the top of the screen, ensuring it doesn't get hidden behind background tabs while multitasking.

## Tech Stack

* **Language:** Python 3.10+
* **Computer Vision:** OpenCV (`opencv-python`)
* **Hand Tracking & AI:** Google MediaPipe (`mediapipe`)
* **System Automation:** PyAutoGUI (`pyautogui`)
* **Math & Logic:** Core Python `math` and `time` modules for distance calculation and action cooldowns.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/AI-Gesture-Mouse.git](https://github.com/YourUsername/AI-Gesture-Mouse.git)
   ```
   *(Note: Replace `YourUsername` with your actual GitHub username)*

2. **Navigate to the project directory:**
   ```bash
   cd AI-Gesture-Mouse
   ```

3. **Install the required dependencies:**
   Make sure you have Python 3.10 or above installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is not available, install manually: `pip install opencv-python mediapipe pyautogui`)*

##    How to Use

Run the main script from your terminal:
```bash
python Hand_Gesture.py
```

* **Tips for Best Performance:** 
  * Ensure you are in a well-lit environment.
  * Keep your hand clearly visible within the camera frame.
  * Avoid sudden, jerky movements for smoother cursor control.
* **To Exit:** Press the `q` key while the camera window is active to safely terminate the program.

---
**Developed by:** Khan Mustafa
