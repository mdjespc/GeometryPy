
import pygame

class Object(pygame.sprite.Sprite):
    '''
    Parent class to all obstacle classes, and its children.
    '''
    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        for group in groups:
            group.add(self)
    
    def update(self, *args, **kwargs):
        self.rect.x -= 3


    def draw(self, surf):
        surf.blit(self.image, self.rect)
  


'''
||Children Classes
'''
class Block(Object):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Spike(Object):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class Orb(Object):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)