# Hand Controlled Cursor
- An application programmed in PyCharm using Python to capture live video inputs of the user’s hand gesture through a webcam using OpenCV 

- The program then uses the hand-recognition framework by Mediapipe to track the user’s gesture, hand’s landmark and localize 21 coordinates of the hands

- Using the 4th (the thumb’s tip) and the 8th (the index’s tip) coordinates, the mouse cursor moves accordingly to the middle of these two coordinates. When the space between two points falls below a certain threshold, it registers as a click command
