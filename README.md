# Gesture-Driven-Presentation-Controller

This project allows users to control and navigate presentation slides using hand gestures. By utilizing real-time hand tracking, users can interact with the slides, draw annotations, and use a laser pointer, all without touching a keyboard or mouse.

## Features

- **Gesture-Based Slide Navigation:** Move through presentation slides by detecting hand gestures such as thumb extension and all fingers open.
- **Real-Time Hand Tracking:** Uses the `cvzone` Hand Tracking Module for precise hand gesture recognition.
- **Laser Pointer:** Activate a laser pointer with a specific hand gesture for highlighting areas of the presentation.
- **Annotation Drawing:** Draw directly on slides with hand gestures to annotate content during presentations.
- **Persistent Annotations:** Save and load annotations using JSON for future sessions.

## Tech Stack

- **Python**
- **OpenCV** (cv2)
- **cvzone** (for Hand Tracking)
- **NumPy**
- **JSON**

## Installation

1. Clone the repository:
   git clone https://github.com/NavjotKaurCheema/Gesture-Driven-Presentation-Controller
2. Navigate to the project directory:
   cd Gesture-Driven-Presentation-Controller
3. Install the required dependencies:
   pip install opencv-python numpy cvzone

## Usage

1. Place your presentation images in the `Presentation` folder.
2. Run the script:
   python main.py
3. Use hand gestures to navigate the presentation:
   - **Thumb extended** to move to the previous slide.
   - **All fingers open** to move to the next slide.
   - **Pointing gesture** to activate the laser pointer.
   - **Drawing gesture** to annotate the slide.

## Notes

- The webcam feed will be displayed in the bottom right corner of the screen.
- Annotations are saved in a JSON file for future use.
