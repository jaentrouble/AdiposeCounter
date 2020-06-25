import pygame
import numpy as np
from queue import Queue

class Viewer() :
    """
    This module shows a numpy array(3D) on a display
    """
    def __init__(self, width:int, height:int, event_queue:Queue,
                 image_queue:Queue):
        """
        Initialize Viewer

        Arguments:
        width : Width of the screen (Default 720)
        height : Height of the screen (Default 720)
        event_queue: a Queue to put events that happended in Viewer
        image_queue: a Queue to get image array
        """
        pygame.init()
        self._width = width
        self._height = height
        self._screen = pygame.display.set_mode((self._width, self._height),
                                                pygame.RESIZABLE)
        self._clock = pygame.time.Clock()
        self._event_queue = event_queue
        self._image_queue = image_queue

    def run(self, initial_image:np.array) :
        """
        Run viewer's mainloop
        """
        mainloop = True
        if initial_image.shape != (self._height, self._width):
            
        if direct :
            pygame.surfarray.blit_array(self._screen, surfarray)
        else :
            surface = pygame.surfarray.make_surface(surfarray)
            self._screen.blit(surface, (0,0))
        pygame.display.flip()

    @property
    def size(self):
        return(self._width, self._height)

    def close(self):
        pygame.quit()

#testing
if __name__ == '__main__':
    import time
    a = np.random.randint(0,255,(720,720,3),dtype=np.uint8)
