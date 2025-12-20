"""
Obstacles module for the racing game
Handles obstacle generation and movement
"""

import pygame
import random
from config import *


class Obstacle:
    def __init__(self, x, y, speed):
        """Initialize an obstacle"""

        self.x = x
        self.y = y
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.speed = speed

        # Random color for variety
        self.color = random.choice([RED, YELLOW, (255, 140, 0), (128, 0, 128)])

        # Create obstacle surface
        self.create_obstacle_surface()

        # Collision rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def create_obstacle_surface(self):
        """Create obstacle sprite (other car)"""

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Car body
        pygame.draw.rect(self.surface, self.color, (5, 10, 40, 60), border_radius=10)

        # Windows (darker shade)
        darker_color = tuple(max(0, c - 50) for c in self.color)
        pygame.draw.rect(self.surface, darker_color, (10, 15, 30, 20), border_radius=5)
        pygame.draw.rect(self.surface, darker_color, (10, 45, 30, 20), border_radius=5)

        # Wheels
        pygame.draw.rect(self.surface, BLACK, (0, 15, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (42, 15, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (0, 50, 8, 15), border_radius=3)
        pygame.draw.rect(self.surface, BLACK, (42, 50, 8, 15), border_radius=3)

    def update(self, dt, player_speed):
        """Update obstacle position"""

        # Move down relative to player speed
        self.y += (self.speed + player_speed * 0.5) * dt

        # Update rectangle
        self.rect.y = self.y

    def draw(self, screen):
        """Draw the obstacle"""
        screen.blit(self.surface, (self.x, self.y))

    def is_off_screen(self):
        """Check if obstacle is off screen"""
        return self.y > SCREEN_HEIGHT


class ObstacleManager:
    def __init__(self):
        """Initialize obstacle manager"""

        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_rate = OBSTACLE_SPAWN_RATE

        # Lane positions
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        self.lanes = [
            road_left + LANE_WIDTH * 0.5 - OBSTACLE_WIDTH // 2,
            road_left + LANE_WIDTH * 1.5 - OBSTACLE_WIDTH // 2,
            road_left + LANE_WIDTH * 2.5 - OBSTACLE_WIDTH // 2
        ]

    def update(self, dt, player_speed):
        """Update all obstacles"""

        # Update spawn timer
        self.spawn_timer += dt

        # Spawn new obstacles
        if self.spawn_timer >= self.spawn_rate and len(self.obstacles) < MAX_OBSTACLES:
            self.spawn_obstacle()
            self.spawn_timer = 0

            # Increase difficulty over time
            self.spawn_rate = max(0.8, self.spawn_rate - 0.01)

        # Update existing obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(dt, player_speed)

            # Remove off-screen obstacles
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

    def spawn_obstacle(self):
        """Spawn a new obstacle"""

        # Choose random lane
        lane = random.choice(self.lanes)

        # Random speed variation
        speed = OBSTACLE_SPEED + random.randint(-50, 50)

        # Create obstacle above screen
        obstacle = Obstacle(lane, -OBSTACLE_HEIGHT - 20, speed)
        self.obstacles.append(obstacle)

    def draw(self, screen):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def check_collision(self, player_rect):
        """Check collision with player"""

        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.obstacles.remove(obstacle)
                return True

        return False

    def reset(self):
        """Reset obstacle manager"""
        self.obstacles.clear()
        self.spawn_timer = 0
        self.spawn_rate = OBSTACLE_SPAWN_RATE