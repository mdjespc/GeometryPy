import pygame

AVATAR_IMAGE = pygame.transform.scale(pygame.image.load("sprites\\images\\avatar.png"), (32, 32))

class Avatar(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos

    def update(self, pos, *args, **kwargs):
        self.pos = pos
        pass

    def draw(self, surf):
        surf.blit(self.image, self.pos)