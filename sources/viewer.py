import pygame
import numpy as np
from multiprocessing import Queue
from multiprocessing import Process
from .common.constants import *

class Viewer(Process) :
    """
    This module shows a numpy array(3D) on a display
    """
    def __init__(self, width:int, height:int, event_queue:Queue,
                 image_queue:Queue, etc_queue:Queue, termQ:Queue,
                 fps=60):
        """
        Initialize Viewer

        Arguments:
        width : Width of the screen (Default 720)
        height : Height of the screen (Default 720)
        event_queue: a Queue to put events that happended in Viewer
        image_queue: a Queue to get image array
        etc_queue: a Queue to get any meta info
        """
        super().__init__(daemon=True)
        self.size = (width, height)
        self._event_queue = event_queue
        self._image_queue = image_queue
        self._etc_queue = etc_queue
        self._fps = fps
        self._put_mouse_pos = False
        self._termQ = termQ

    def run(self) :
        """
        Run viewer's mainloop
        """
        mainloop = True
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        while mainloop :
            self._clock.tick(self._fps)
            if not self._image_queue.empty():
                image = self._image_queue.get()
                if image.shape[0:2] != self.size:
                    self.size = image.shape[0:2]
                    self._screen = pygame.display.set_mode(self.size)
                pygame.surfarray.blit_array(self._screen, image)
            if not self._etc_queue.empty():
                q = self._etc_queue.get()
                for k,v in q.items():
                    if k == TERMINATE:
                        mainloop=False
                    elif k == MOUSEPOS_ON:
                        self._put_mouse_pos = True
                    elif k == MOUSEPOS_OFF:
                        self._put_mouse_pos = False
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
            ######################################
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self._event_queue.put({MOUSEDOWN:pygame.mouse.get_pos()})

            if self._put_mouse_pos:
                self._event_queue.put({MOUSEPOS:pygame.mouse.get_pos()})
            pygame.display.flip()
        self._termQ.put(TERMINATE)

    @property
    def size(self):
        """
        size : (width, height)
        """
        return (self._width, self._height)

    @size.setter
    def size(self, size:tuple):
        """
        size : (width, height)
        """
        self._width, self._height = size

    def close(self):
        pygame.quit()




# Constants ###################################################################





#testing
if __name__ == '__main__':
    import time
    imgQ = Queue()
    evntQ = Queue()
    etcQ = Queue()
    v = Viewer(720, 300, evntQ, imgQ, etcQ)
    v.start()
    time.sleep(3)
    newimg = np.ones((600,600,3), dtype=np.uint8)*100
    imgQ.put(newimg)
    time.sleep(3)