"""
Car class for the racing game
Handles car physics and rendering
"""

import pygame
import math
from config import *


class Car:
    def __init__(self, x, y):
        """Initialize the car"""

        self.x = x
        self.y = y
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.speed = 0
        self.max_speed = CAR_MAX_SPEED
        self.acceleration = CAR_ACCELERATION
        self.friction = CAR_FRICTION

        # Create car surface
        self.create_car_surface()

        # Collision rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Collision cooldown
        self.collision_timer = 0
        self.can_collide = True

    def create_car_surface(self):
        """Create a simple car sprite"""

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Car body (blue)
        pygame.draw.rect(self.surface, BLUE, (5, 10, 40, 60), border_radius=10)

        # Car windows (light blue)
        pygame.draw.rect(self.surface, (100, 150, 255), (10, 15, 30, 20), border_radius=5)
        pygame.draw.rect(self.surface, (100, 150, 255), (10, 45, 30, 20), border_radius=5)

        # Wheels (black)
        pygame.draw.rect(self.surface, BLACK, (0, 15, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (42, 15, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (0, 50, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (42, 50, 8, 15), border_radius=3)

        # Headlights (yellow)
        pygame.draw.circle(self.surface, YELLOW, (15, 5), 3)
        pygame.draw.circle(self.surface, YELLOW, (35, 5), 3)

    def update(self, dt, gesture_data):
        """Update car position and physics"""

        # Update collision timer
        if self.collision_timer > 0:
            self.collision_timer -= dt
            if self.collision_timer <= 0:
                self.can_collide = True

        # Handle acceleration
        if gesture_data['acceleration'] > 0:
            self.speed += self.acceleration * gesture_data['acceleration'] * dt
        else:
            # Apply friction
            if self.speed > 0:
                self.speed -= self.friction * dt
                self.speed = max(0, self.speed)

        # Limit speed
        self.speed = min(self.speed, self.max_speed)

        # Handle steering
        steering = gesture_data['steering']
        if steering != 0:
            self.x += steering * STEERING_SPEED * dt

        # Keep car on road
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - self.width

        self.x = max(road_left, min(self.x, road_right))

        # Update rectangle
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        """Draw the car"""

        # Flash red when in collision cooldown
        if not self.can_collide and int(self.collision_timer * 10) % 2 == 0:
            # Create red tint
            tinted_surface = self.surface.copy()
            red_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            tinted_surface.blit(red_overlay, (0, 0))
            screen.blit(tinted_surface, (self.x, self.y))
        else:
            screen.blit(self.surface, (self.x, self.y))

    def handle_collision(self):
        """Handle collision with obstacle"""

        if self.can_collide:
            self.collision_timer = COLLISION_COOLDOWN
            self.can_collide = False
            self.speed = 0
            return True
        return False

    def get_speed_percentage(self):
        """Get speed as percentage of max speed"""
        return (self.speed / self.max_speed) * 100