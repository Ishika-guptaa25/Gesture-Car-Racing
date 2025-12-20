import pygame
import sys
from game import Game
from gesture_controller import GestureController
from config import *


def main():
    """Main game loop"""

    # Initialize Pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🚗 Hand Gesture Car Racing")

    # Set icon (optional)
    try:
        icon = pygame.image.load('assets/car.png')
        pygame.display.set_icon(icon)
    except:
        print("⚠️ Could not load icon")

    # Initialize game components
    clock = pygame.time.Clock()
    game = Game(screen)
    gesture_controller = GestureController()

    # Game state
    running = True
    paused = False
    show_camera = True

    print("=" * 50)
    print("🎮 HAND GESTURE CAR RACING GAME")
    print("=" * 50)
    print("\n📋 Controls:")
    print("  • Tilt hand LEFT/RIGHT → Steer")
    print("  • Palm FORWARD → Accelerate")
    print("  • SPACE → Pause/Resume")
    print("  • C → Toggle Camera View")
    print("  • ESC → Quit")
    print("\n✅ Game Started! Show your hand to the camera.")
    print("=" * 50 + "\n")

    # Main game loop
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    print(f"⏸️  Game {'Paused' if paused else 'Resumed'}")
                elif event.key == pygame.K_c:
                    show_camera = not show_camera
                    print(f"📷 Camera view: {'ON' if show_camera else 'OFF'}")
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
                    print("🔄 Game Reset!")

        # Get gesture input
        gesture_data = gesture_controller.get_gesture()

        if not paused and not game.game_over:
            # Update game with gesture data
            game.update(dt, gesture_data)

        # Draw everything
        game.draw()

        # Draw camera feed if enabled
        if show_camera:
            camera_surface = gesture_controller.get_camera_surface()
            if camera_surface:
                screen.blit(camera_surface, (SCREEN_WIDTH - 220, 10))

        # Draw pause overlay
        if paused:
            draw_pause_overlay(screen)

        # Update display
        pygame.display.flip()

    # Cleanup
    print("\n🛑 Shutting down...")
    gesture_controller.release()
    pygame.quit()
    sys.exit()


def draw_pause_overlay(screen):
    """Draw pause overlay"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 74)
    text = font.render("PAUSED", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    text2 = font_small.render("Press SPACE to resume", True, WHITE)
    text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(text2, text2_rect)


if __name__ == "__main__":
    main()