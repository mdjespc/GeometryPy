from pygame.math import Vector2
import pygame

def rotate_sprite(surf, image, pos, originpos, angle):
    """
    Rotates a sprite image around an origin position by a specified angle
    and blits it onto the provided surface.

    Args:
        surf (pygame.Surface): The surface to draw on.
        image (pygame.Surface): The sprite image to rotate.
        pos (tuple): The position to rotate around (x, y).
        originpos (tuple): The origin point within the sprite (x, y).
        angle (float): The angle of rotation in degrees.

    Returns:
        None
    """
    w, h = image.get_size()
    box = [Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]

    # Calculate the bounding box
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # Calculate the translation of the pivot
    pivot = Vector2(originpos[0], -originpos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # Calculate the origin of the rotated image
    origin = (pos[0] - originpos[0] + min_box[0] - pivot_move[0],
              pos[1] - originpos[1] - max_box[1] + pivot_move[1])

    # Get a rotated image and blit it
    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    surf.blit(rotated_image, origin)
