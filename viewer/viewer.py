import pygame
import numpy as np
from multiprocessing import Queue
from multiprocessing import Process

class Viewer(Process) :
    """
    This module shows a numpy array(3D) on a display
    String 'Terminate' will terminate the viewer
    """
    def __init__(self, width:int, height:int, event_queue:Queue,
                 image_queue:Queue, etc_queue:Queue, fps=60):
        """
        Initialize Viewer

        Arguments:
        width : Width of the screen (Default 720)
        height : Height of the screen (Default 720)
        event_queue: a Queue to put events that happended in Viewer
        image_queue: a Queue to get image array
        etc_queue: a Queue to get any info like 'terminate'
        """
        super().__init__(daemon=True)
        self.size = (width, height)
        self._event_queue = event_queue
        self._image_queue = image_queue
        self._etc_queue = etc_queue
        self._fps = fps

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
                external_event = self._etc_queue.get()
                if external_event == 'Terminate' :
                    mainloop = False
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
                        return
            ######################################          
        # if direct :
        #     pygame.surfarray.blit_array(self._screen, surfarray)
        # else :
        #     surface = pygame.surfarray.make_surface(surfarray)
        #     self._screen.blit(surface, (0,0))
            pygame.display.flip()

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