"""
Gesture Controller Module
Handles hand gesture detection using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
import pygame
from config import *


class GestureController:
    def __init__(self):
        """Initialize gesture controller with MediaPipe"""

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=HAND_TRACKING_CONFIDENCE
        )

        # Initialize camera
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        # Gesture data
        self.steering = 0.0  # -1 (left) to 1 (right)
        self.acceleration = 0.0  # 0 to 1

        # Camera frame for display
        self.camera_frame = None

        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("⚠️ Warning: Could not open camera!")
            print("📝 Game will run with keyboard controls")

    def get_gesture(self):
        """Process camera frame and detect gestures"""

        if not self.cap.isOpened():
            return self._get_keyboard_input()

        success, frame = self.cap.read()

        if not success:
            return self._get_keyboard_input()

        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame
        results = self.hands.process(rgb_frame)

        # Reset gestures
        self.steering = 0.0
        self.acceleration = 0.0

        # If hand detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                # Calculate gestures
                self._calculate_steering(hand_landmarks)
                self._calculate_acceleration(hand_landmarks)

        # Store frame for display
        self.camera_frame = frame

        return {
            'steering': self.steering,
            'acceleration': self.acceleration
        }

    def _calculate_steering(self, hand_landmarks):
        """Calculate steering based on hand tilt"""

        # Get wrist and middle finger tip
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # Calculate horizontal tilt
        tilt = middle_tip.x - wrist.x

        # Apply thresholds and normalize
        if tilt < TILT_LEFT_THRESHOLD:
            self.steering = -1.0
        elif tilt > TILT_RIGHT_THRESHOLD:
            self.steering = 1.0
        else:
            # Smooth steering in deadzone
            normalized_tilt = (tilt - TILT_LEFT_THRESHOLD) / (TILT_RIGHT_THRESHOLD - TILT_LEFT_THRESHOLD)
            self.steering = (normalized_tilt * 2) - 1
            self.steering = max(-1.0, min(1.0, self.steering))

    def _calculate_acceleration(self, hand_landmarks):
        """Calculate acceleration based on palm forward gesture"""

        # Get palm landmarks
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

        # Calculate Z-axis distance (depth)
        palm_depth = abs(wrist.z - middle_mcp.z)

        # Check if palm is facing forward
        if palm_depth > PALM_FORWARD_THRESHOLD:
            self.acceleration = 1.0
        else:
            # Gradual acceleration
            self.acceleration = min(1.0, palm_depth / PALM_FORWARD_THRESHOLD)

    def _get_keyboard_input(self):
        """Fallback keyboard controls"""

        keys = pygame.key.get_pressed()

        steering = 0.0
        acceleration = 0.0

        # Arrow keys for steering
        if keys[pygame.K_LEFT]:
            steering = -1.0
        elif keys[pygame.K_RIGHT]:
            steering = 1.0

        # Up arrow for acceleration
        if keys[pygame.K_UP]:
            acceleration = 1.0

        return {
            'steering': steering,
            'acceleration': acceleration
        }

    def get_camera_surface(self):
        """Convert camera frame to pygame surface for display"""

        if self.camera_frame is None:
            return None

        # Resize for display
        small_frame = cv2.resize(self.camera_frame, (200, 150))

        # Convert to RGB for pygame
        frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Rotate 90 degrees and flip
        frame_rgb = np.rot90(frame_rgb)

        # Convert to pygame surface
        surface = pygame.surfarray.make_surface(frame_rgb)

        return surface

    def release(self):
        """Release camera resources"""

        if self.cap.isOpened():
            self.cap.release()

        self.hands.close()
        print("✅ Camera released")