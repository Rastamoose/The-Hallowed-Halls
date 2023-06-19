import pygame
from pygame.locals import *


#----------handles speech with text box-----------#
def dialogue(display, speaking, font, name_colour, text_colour, FPS, time, text_timer, name, text, text_box, text_box_pos = (100,480)):
  name_font = pygame.font.Font(font, 30)
  text_font = pygame.font.Font(font, 24)                    #sets up name and text fonts based on arguments passed in to function
  name = name_font.render(str(name), True, name_colour)
  display.blit(text_box, text_box_pos)

  if text_timer[0] != time*60:          # timer in seconds for how long text should stay on screen for
    speech = text_font.render(text[text_timer[1]], True, text_colour) # render text based on where it is in the list (text_timer[1] starts at 0)
    text_timer[0] += 1      #adds to timer every iteration
    speaking = True

    text_box_rect = text_box.get_rect(topleft=(100, 480))
    display.blit(name, (text_box_rect.x+40, text_box_rect.y+12))      #displays text and speech
    display.blit(speech, (text_box_rect.x+30, text_box_rect.y+90))
  else:
    text_timer[0] = 0               # if the amount of seconds that a line has to be displayed for is up, it resets the timer and adds to the list number
    text_timer[1] += 1    

 
  if text_timer[1] >= len(text):
    text_timer[1] = 0
    speaking = False            # if you get to the end of the list the list number gets reset to zero and the speech stops using speaking var
  else:
    speaking = True

  return speaking, text_timer


def basic_text(display, font, colour, size, loc, scroll, text, lines):
  new_text = text.split(" ")
  length_to_split = (len(new_text))//lines
  split_text = []                               #gets length to split text at and text remaining after split depending on amount of lines
  length_remainder = (len(new_text)) % lines

  while len(new_text) != 0:     #keeps iterating until there is no text left to seperate
    text_to_append = []                           
    for i in range(length_to_split):
      text_to_append.append(new_text[0])          #sorts text into different lists based on which line it is
      new_text.remove(new_text[0])
    split_text.append(text_to_append)

    if len(new_text) == length_remainder:     #if there are no lines left, only remainder text
      text_to_append = []
      for i in range(length_remainder):
        text_to_append.append(new_text[0])      #sorts remainder text into a line
        new_text.remove(new_text[0])
      split_text.append(text_to_append)

  font = pygame.font.Font(font, size)
  line_distance = 0
  for i in split_text:
    if i != []:
      text_to_render = str(i)
      text_to_render = text_to_render.replace("[", "")
      text_to_render = text_to_render.replace("]", "")      #takes text from list and strips it of list attributes ([, ], ', ')
      text_to_render = text_to_render.replace("'", "")
      text_to_render = text_to_render.replace(",", "")
      render_text = font.render(text_to_render, True, colour)
      loc[1] += line_distance*size                                      #blits text on a new line with the distance between lines being the font size
      display.blit(render_text, (loc[0]-scroll[0], loc[1]-scroll[1]))
      if line_distance == 0:  
        line_distance += 1        #adds to the line distance every new line

