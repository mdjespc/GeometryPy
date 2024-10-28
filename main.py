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

#Load level songs
level_1_song = "music/mortals.mp3"
level_2_song = ""

pygame.mixer.init()
pygame.mixer.music.load(level_1_song)
pygame.mixer.music.play()


#Constants
GRAVITY = Vector2(0, 0.86)
FPS = 60

#Load background and player image
BACKGROUND_IMAGE = pygame.image.load("sprites\\images\\bg.png")

player_group = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
  '''
  Controls an Avatar object, whose position is dictated by
  an instance of this class. 

  Also handles in-game conditions & events that interact
  with the avatar.
  '''
  is_jumping: bool
  is_grounded: bool

  def __init__(self, image, pos):
    super().__init__()
    self.image = image
    self.pos = pos
    #self.avatar = Avatar(self.image, self.pos)
    self.rect = self.image.get_rect()

    self.vel = Vector2(0, 0)
    self.jump_height = -12
    self.is_jumping = False
    self.is_grounded = False
    
  def jump(self):
    self.vel.y = self.jump_height
    print("jump function")

  def check_collisions(self, level: Level):
    collided_sprite = pygame.sprite.spritecollideany(self, level.all_elements)
    if collided_sprite:
      if isinstance(collided_sprite, Block):
        #Snap player to the collided block
        self.rect.bottom = collided_sprite.rect.top
        self.is_grounded = True
        return
      elif isinstance(collided_sprite, Spike):
        pass
      elif isinstance(collided_sprite, Orb):
        self.vel.y = self.jump_height * 2
    
    self.is_grounded = False


  def update(self):
    if self.is_grounded:
      if self.is_jumping:
        self.jump()
      else:
        self.vel.y = 0
      self.is_jumping = False
    else:
      self.vel.y = min(self.vel.y + GRAVITY.y, 16) #Hardcapping falling speed at 16.
      

    #Update the position the avatar should have
    self.pos = (self.pos[0], self.pos[1] + self.vel.y)
    self.rect.x = self.pos[0]
    self.rect.y = self.pos[1]
    #self.avatar.update(self.pos)

  def draw(self, surf):
    #self.avatar.draw(surf)
    if not self.is_jumping:
      surf.blit(self.image, self.pos)
    pygame.draw.rect(surf, "white", self.rect, 5)


def rotate_sprite(surf, image, pos, originpos, angle):
  w, h = image.get_size()
  box = [Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
  box_rotate = [p.rotate(angle) for p in box]

  # make sure the player does not overlap, uses a few lambda functions(new things that we did not learn about number1)
  min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
  max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
  # calculate the translation of the pivot
  pivot = Vector2(originpos[0], -originpos[1])
  pivot_rotate = pivot.rotate(angle)
  pivot_move = pivot_rotate - pivot

  # calculate the upper left origin of the rotated image
  origin = (pos[0] - originpos[0] + min_box[0] - pivot_move[0], pos[1] - originpos[1] - max_box[1] + pivot_move[1])

  # get a rotated image
  rotated_image = pygame.transform.rotozoom(image, angle, 1)

  # rotate and blit the image
  surf.blit(rotated_image, origin)


TEST_PLAYER = Player(AVATAR_IMAGE, (width//2, height//2))
#player_group.add(TEST_PLAYER.avatar)
TEST_LEVEL = Level(1)
TEST_LEVEL.load_file()
TEST_LEVEL.load_elements()

angle = 0

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
  if TEST_PLAYER.is_jumping:
    angle -= 8.1712
    rotate_sprite(surf, TEST_PLAYER.image, TEST_PLAYER.rect.center, (16, 16), angle)

  TEST_PLAYER.check_collisions(TEST_LEVEL)
 

  TEST_PLAYER.draw(surf)

  for element in TEST_LEVEL.level_elements:
    element.draw(surf)

  clock.tick(FPS)
  pygame.display.update()


