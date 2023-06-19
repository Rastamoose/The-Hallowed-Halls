import pygame, time
import data.modules.noise as noise
from pygame.locals import *
from abc import ABC, abstractmethod


#-----------------class for camera------------------#
class camera:
  def __init__(self, player, display):
    self.player = player
    self.offset = pygame.math.Vector2(0,0)
    self.offself_float = pygame.math.Vector2(0,0)
    self.display = display
    self.constant = pygame.math.Vector2(0,0)
    
    def set_method(self, method):
      self.method = method
      
    def scroll(self):
      self.method.scroll()
    
class camscroll(ABC):
  def __init__(self, camera, player):
    self.camera = camera
    self.player = player
    
  @abstractmethod
  def scroll(self):
    pass

