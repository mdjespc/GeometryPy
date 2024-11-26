import pygame
import csv
from sprites.objects import *

#Load all level object images
BLOCK_IMAGE = pygame.transform.scale(pygame.image.load("sprites\\images\\block_1.png"), (32, 32))
SPIKE_IMAGE = pygame.transform.scale(pygame.image.load("sprites\\images\\obj-spike.png"), (32, 32))
YELLOW_ORB_IMAGE = pygame.transform.scale(pygame.image.load("sprites\\images\\orb-yellow.png"), (32, 32))

class Level:
    '''
    Reads through CSV-based level files and determines
    the order in which level sprite objects should be
    rendered.
    '''
    def __init__(self, level_id):
        self.level_path = f"levels\\level_{level_id}.csv"
        self.level_elements = []
        self.all_elements = pygame.sprite.Group()
        self.all_blocks = pygame.sprite.Group()
        self.all_spikes = pygame.sprite.Group()
        self.all_orbs = pygame.sprite.Group()
    
    def load_file(self):
        '''
        Open the csv file and load its elements onto a list
        '''
        self.level_list = []
        try:
            with open(self.level_path, newline='') as csvfile:
                file = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in file:
                    self.level_list.append(row)
        except FileNotFoundError as err:
            print("Error loading level file:", err)

    
    def load_elements(self):
        '''
        Map all file elements into objects. Once all elements are loaded,
        they can be rendered using the render() method
        '''
        if not self.level_list:
            print('''
                  Level file contains no elements. 
                  This could be due to a failure while loading the level file.
                  ''')
            return
        
        
        for row, elements in enumerate(self.level_list):
            for column, element_id in enumerate(elements):
                pos = (column * 32, row * 32)
                if element_id == "-1": pass
                elif element_id == "0":
                    obj = Block(BLOCK_IMAGE, pos, self.all_elements, self.all_blocks)
                    self.level_elements.append(
                        obj
                        ) 
                    self.all_elements.add(obj)
                    self.all_blocks.add(obj)
                elif element_id == "1":
                    obj = Spike(SPIKE_IMAGE, pos, self.all_elements, self.all_spikes)
                    self.level_elements.append(
                        obj
                        )
                    self.all_elements.add(obj)
                    self.all_spikes.add(obj)
                elif element_id == "2":
                    obj = Orb(YELLOW_ORB_IMAGE, pos, self.all_elements, self.all_orbs)
                    self.level_elements.append(
                        obj
                        )
                    self.all_elements.add(obj)
                    self.all_orbs.add(obj)
        
    def clear(self):
        self.level_elements.clear()
        self.all_elements.empty()
        self.all_blocks.empty()
        self.all_spikes.empty()
        self.all_orbs.empty()

