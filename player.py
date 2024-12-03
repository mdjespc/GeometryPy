import pygame
from pygame.math import Vector2
from levels.level import Level
from sprites.objects import Block, Spike, Orb

# Constants
GRAVITY = Vector2(0, 0.86)
JUMP_HEIGHT = -12
MAX_FALL_SPEED = 16

class Player(pygame.sprite.Sprite):
    """
    Controls an Avatar object, whose position is dictated by
    an instance of this class. 

    Also handles in-game conditions & events that interact
    with the avatar.
    """
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect()
        self.vel = Vector2(0, 0)

        self.is_jumping = False
        self.is_grounded = False
        self.is_destroyed = False

    def jump(self):
        self.vel.y = JUMP_HEIGHT

    def set_destroyed(self, is_destroyed: bool):
        self.is_destroyed = is_destroyed

    def reset_pos(self, screen_width, screen_height):
        self.pos = (screen_width // 2, screen_height // 2)

    def resolve_collisions(self, level: Level):
        collided_sprite = pygame.sprite.spritecollideany(self, level.all_elements)
        if collided_sprite:
            if isinstance(collided_sprite, Block):
                # Kill player if collided from the side of the block
                if self.rect.y >= collided_sprite.rect.top:
                    self.set_destroyed(True)

                # Snap player to the collided block
                self.rect.bottom = collided_sprite.rect.top
                self.is_grounded = True
                return
            elif isinstance(collided_sprite, Spike):
                self.set_destroyed(True)
            elif isinstance(collided_sprite, Orb):
                # Potential feature: Modify player jump height
                pass
        else:
            self.is_grounded = False

    def update(self):
        if self.is_grounded:
            if self.is_jumping:
                self.jump()
            else:
                self.vel.y = 0
            self.is_jumping = False
        else:
            self.vel.y = min(self.vel.y + GRAVITY.y, MAX_FALL_SPEED)

        # Update position
        self.pos = (self.pos[0], self.pos[1] + self.vel.y)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self, surf):
        surf.blit(self.image, self.rect)
