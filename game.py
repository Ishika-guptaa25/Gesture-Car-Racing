"""
Main Game class
Handles game logic, rendering, and state management
"""

import pygame
from car import Car
from obstacles import ObstacleManager
from config import *

class Game:
    def __init__(self, screen):
        """Initialize the game"""

        self.screen = screen

        # Game state
        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_over = False
        self.distance = 0

        # Road animation
        self.road_offset = 0

        # Initialize player car
        car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
        car_y = SCREEN_HEIGHT - CAR_HEIGHT - 50
        self.player = Car(car_x, car_y)

        # Initialize obstacles
        self.obstacle_manager = ObstacleManager()

        # Fonts
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_tiny = pygame.font.Font(None, FONT_TINY)

    def update(self, dt, gesture_data):
        """Update game state"""

        if self.game_over:
            return

        # Update player
        self.player.update(dt, gesture_data)

        # Update road animation
        self.road_offset += (OBSTACLE_SPEED + self.player.speed * 0.5) * dt
        if self.road_offset > LINE_HEIGHT + LINE_GAP:
            self.road_offset = 0

        # Update obstacles
        self.obstacle_manager.update(dt, self.player.speed)

        # Check collisions
        if self.obstacle_manager.check_collision(self.player.rect):
            if self.player.handle_collision():
                self.lives -= 1
                print(f"💥 Crash! Lives remaining: {self.lives}")

                if self.lives <= 0:
                    self.game_over = True
                    print(f"🏁 Game Over! Final Score: {self.score}")

        # Update score and distance
        self.score += int(self.player.speed * dt * SCORE_MULTIPLIER)
        self.distance += self.player.speed * dt / 100

    def draw(self):
        """Draw everything"""

        # Draw grass background
        self.screen.fill(GRASS_COLOR)

        # Draw road
        self.draw_road()

        # Draw obstacles
        self.obstacle_manager.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        # Draw game over screen
        if self.game_over:
            self.draw_game_over()

    def draw_road(self):
        """Draw the road with lane markings"""

        road_x = (SCREEN_WIDTH - ROAD_WIDTH) // 2

        # Draw road
        pygame.draw.rect(self.screen, ROAD_COLOR,
                         (road_x, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # Draw road borders
        pygame.draw.rect(self.screen, YELLOW,
                         (road_x - 5, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, YELLOW,
                         (road_x + ROAD_WIDTH, 0, 5, SCREEN_HEIGHT))

        # Draw lane markings
        for lane in range(1, 3):
            lane_x = road_x + lane * LANE_WIDTH

            # Animated dashed lines
            y = -self.road_offset
            while y < SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, LINE_COLOR,
                                 (lane_x - LINE_WIDTH // 2, y,
                                  LINE_WIDTH, LINE_HEIGHT))
                y += LINE_HEIGHT + LINE_GAP

    def draw_hud(self):
        """Draw heads-up display"""

        # Background panel
        panel_height = 100
        panel = pygame.Surface((SCREEN_WIDTH, panel_height))
        panel.set_alpha(200)
        panel.fill(BLACK)
        self.screen.blit(panel, (0, 0))

        # Score
        score_text = self.font_small.render(f"Score: {self.score:,}", True, WHITE)
        self.screen.blit(score_text, (20, 15))

        # Distance
        distance_text = self.font_tiny.render(f"Distance: {self.distance:.1f}m", True, WHITE)
        self.screen.blit(distance_text, (20, 50))

        # Lives
        lives_text = self.font_small.render(f"Lives:", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 180, 15))

        for i in range(self.lives):
            pygame.draw.circle(self.screen, RED,
                               (SCREEN_WIDTH - 100 + i * 30, 30), 10)

        # Speed meter
        speed_pct = self.player.get_speed_percentage()
        speed_text = self.font_tiny.render(f"Speed: {int(speed_pct)}%", True, WHITE)
        self.screen.blit(speed_text, (SCREEN_WIDTH - 180, 55))

        # Speed bar
        bar_width = 150
        bar_height = 15
        bar_x = SCREEN_WIDTH - 180
        bar_y = 75

        pygame.draw.rect(self.screen, DARK_GRAY,
                         (bar_x, bar_y, bar_width, bar_height))

        speed_width = int((speed_pct / 100) * bar_width)

        # Color based on speed
        if speed_pct < 33:
            speed_color = GREEN
        elif speed_pct < 66:
            speed_color = YELLOW
        else:
            speed_color = RED

        pygame.draw.rect(self.screen, speed_color,
                         (bar_x, bar_y, speed_width, bar_height))

        pygame.draw.rect(self.screen, WHITE,
                         (bar_x, bar_y, bar_width, bar_height), 2)

    def draw_game_over(self):
        """Draw game over screen"""

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)

        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score:,}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        # Distance
        distance_text = self.font_small.render(f"Distance: {self.distance:.1f}m", True, WHITE)
        dist_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(distance_text, dist_rect)

        # Restart instruction
        restart_text = self.font_small.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)

        # Quit instruction
        quit_text = self.font_small.render("Press ESC to Quit", True, GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        self.screen.blit(quit_text, quit_rect)

    def reset(self):
        """Reset the game"""

        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_over = False
        self.distance = 0
        self.road_offset = 0

        # Reset player
        car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
        car_y = SCREEN_HEIGHT - CAR_HEIGHT - 50
        self.player = Car(car_x, car_y)

        # Reset obstacles
        self.obstacle_manager.reset()
