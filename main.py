import sys
import pygame
from pygame.locals import QUIT
from pygame.time import Clock
from pygame.math import Vector2
from sprites.objects import *
from sprites.avatar import Avatar
from sprites.avatar import AVATAR_IMAGE
from levels.level import Level

pygame.init()
clock = Clock()
width, height = 512, 500
surf = pygame.display.set_mode((width, height))


#Constants
GRAVITY = Vector2(0, 0.86)
FPS = 60

#Load background and player image
BACKGROUND_IMAGE = pygame.image.load("sprites\\images\\bg.png")

player_group = pygame.sprite.Group()

class Player:
  '''
  Controls an Avatar object, whose position is dictated by
  an instance of this class. 

  Also handles in-game conditions & events that interact
  with the avatar.
  '''
  is_jumping: bool
  is_grounded: bool

  def __init__(self, image, pos):
    self.image = image
    self.pos = pos
    self.avatar = Avatar(self.image, self.pos)
    self.rect = self.image.get_rect()

    self.vel = Vector2(0, 0)
    self.jump_height = 32
    self.is_jumping = False
    self.is_grounded = False
    
  def jump(self):
    self.vel.y = -self.jump_height

  def check_collisions(self, level: Level):
    for obj in level.all_elements:
      if pygame.Rect.colliderect(self.rect, obj.rect):
        self.is_grounded = True
        print("Collided!")
        return
    self.is_grounded = False


  def update(self):
    if self.is_jumping and self.is_grounded:
      self.jump()

    if not self.is_grounded:
      self.vel.y = min(self.vel.y + GRAVITY.y, 50) #Hardcapping falling speed at 50.
    else:
      self.vel.y = -self.vel.y

    #Update the position the avatar should have
    self.pos = (self.pos[0], self.pos[1] + self.vel.y)
    self.rect.x = self.pos[0]
    self.rect.y = self.pos[1]
    self.avatar.update(self.pos)

  def draw(self, surf):
    self.avatar.draw(surf)
    pygame.draw.rect(surf, "white", self.rect, 1)


TEST_PLAYER = Player(AVATAR_IMAGE, (width//2, height//2))
TEST_LEVEL = Level(1)
TEST_LEVEL.load_file()
TEST_LEVEL.load_elements()
while True:
  #Handle Event
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  #Key press listener
  keys = pygame.key.get_pressed()

  if keys[pygame.K_SPACE]:
    TEST_PLAYER.is_jumping = True

  surf.fill((244, 250, 252))
  surf.blit(BACKGROUND_IMAGE, (0, 0))
  for element in TEST_LEVEL.level_elements:
    element.update()

  TEST_PLAYER.update()
  TEST_PLAYER.check_collisions(TEST_LEVEL)
 

  TEST_PLAYER.draw(surf)

  for element in TEST_LEVEL.level_elements:
    element.draw(surf)

  clock.tick(FPS)
  pygame.display.update()


