#!/usr/bin/env python3
"""
AC'S HOLDING SMB3
A minimal Super Mario Bros 3 clone.
Requirements: pygame
Install with: pip install pygame
"""

import pygame
import sys

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60
GRAVITY = 0.8
PLAYER_JUMP = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2
GROUND_HEIGHT = 40
TILE_SIZE = 40

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (139, 69, 19)
BLOCK_BROWN = (160, 82, 45)
PLAYER_RED = (255, 0, 0)
ENEMY_COLOR = (0, 255, 0)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        # Horizontal movement
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, platforms)

        # Vertical movement
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, platforms)

    def collide(self, dx, dy, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat):
                if dx > 0:  # Moving right
                    self.rect.right = plat.left
                elif dx < 0:  # Moving left
                    self.rect.left = plat.right
                elif dy > 0:  # Moving down (falling)
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:  # Moving up (jumping)
                    self.rect.top = plat.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = PLAYER_JUMP

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.direction = 1  # 1 = right, -1 = left
        self.alive = True

    def update(self, platforms):
        if not self.alive:
            return
        self.rect.x += ENEMY_SPEED * self.direction
        # Simple AI: change direction if hitting a wall or falling off a ledge
        for plat in platforms:
            if self.rect.colliderect(plat):
                self.direction *= -1
                break
        # Also turn if at edge of ground (optional)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AC'S HOLDING SMB3")
    clock = pygame.time.Clock()

    # Build a simple level: ground and some blocks
    platforms = []
    # Ground from x=0 to x=2000 (level width)
    for x in range(0, 2000, TILE_SIZE):
        platforms.append(pygame.Rect(x, SCREEN_HEIGHT - GROUND_HEIGHT, TILE_SIZE, GROUND_HEIGHT))

    # Add some floating blocks (like ? blocks)
    platforms.append(pygame.Rect(300, SCREEN_HEIGHT - 150, TILE_SIZE, TILE_SIZE))
    platforms.append(pygame.Rect(340, SCREEN_HEIGHT - 150, TILE_SIZE, TILE_SIZE))
    platforms.append(pygame.Rect(600, SCREEN_HEIGHT - 200, TILE_SIZE, TILE_SIZE))
    platforms.append(pygame.Rect(800, SCREEN_HEIGHT - 250, TILE_SIZE, TILE_SIZE))
    platforms.append(pygame.Rect(1000, SCREEN_HEIGHT - 150, TILE_SIZE, TILE_SIZE))

    # Create player
    player = Player(100, SCREEN_HEIGHT - GROUND_HEIGHT - TILE_SIZE)

    # Create enemies
    enemies = [Enemy(400, SCREEN_HEIGHT - GROUND_HEIGHT - TILE_SIZE)]

    # Camera offset
    camera_x = 0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Continuous key handling
        keys = pygame.key.get_pressed()
        player.vel_x = 0
        if keys[pygame.K_LEFT]:
            player.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.vel_x = PLAYER_SPEED

        # Update objects
        player.update(platforms)
        for enemy in enemies:
            enemy.update(platforms)

        # Check enemy-player collision (simple)
        for enemy in enemies[:]:
            if enemy.alive and player.rect.colliderect(enemy.rect):
                # If player is falling onto enemy, kill enemy
                if player.vel_y > 0 and player.rect.bottom <= enemy.rect.centery + 10:
                    enemy.alive = False
                    player.vel_y = PLAYER_JUMP / 2  # Bounce
                else:
                    # Player gets hurt (here we just reset position)
                    print("Ouch! (Player reset)")
                    player.rect.x = 100
                    player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - TILE_SIZE

        # Remove dead enemies
        enemies = [e for e in enemies if e.alive]

        # Camera follows player (keep player centered)
        camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        # Clamp camera to level boundaries (level width ~2000)
        camera_x = max(0, min(camera_x, 2000 - SCREEN_WIDTH))

        # Draw everything
        screen.fill(SKY_BLUE)

        # Draw platforms
        for plat in platforms:
            screen_rect = plat.move(-camera_x, 0)
            if plat.y > SCREEN_HEIGHT - GROUND_HEIGHT:
                color = GROUND_BROWN
            else:
                color = BLOCK_BROWN
            pygame.draw.rect(screen, color, screen_rect)

        # Draw enemies
        for enemy in enemies:
            screen_rect = enemy.rect.move(-camera_x, 0)
            pygame.draw.rect(screen, ENEMY_COLOR, screen_rect)

        # Draw player
        screen_rect = player.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, PLAYER_RED, screen_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()