import pygame
import numpy as np

class Viewer() :
    """
    This module shows a numpy array(3D) on a display
    """
    def __init__(self, width = 720, height = 720, **kwargs):
        """
        Initialize Viewer

        Arguments:
        width : Width of the screen (Default 720)
        height : Height of the screen (Default 720)
        """
        pygame.init()
        self._width = width
        self._height = height
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()

    @property
    def size(self):
        """
        Returns (width, height)
        """
        return (self._width, self._height)

    def render(self, surfarray, direct=False) :
        """
        Render a np.array on to the screen
        
        surfarray: (type=np.array) An 3D array to blit on the screen
        direct: If True, blits directly on the screen.
                The array's dimensions must be the same as the screen

        Note: It does not check the size of the array
        """
        if direct :
            pygame.surfarray.blit_array(self._screen, surfarray)
        else :
            surface = pygame.surfarray.make_surface(surfarray)
            self._screen.blit(surface, (0,0))
        pygame.display.flip()

    def close(self):
        pygame.quit()

#testing
if __name__ == '__main__':
    import time
    a = np.random.randint(0,255,(720,300,3),dtype=np.uint8)
    print(a.dtype)
    v = Viewer(width=720, height=300)
    v.render(a,True)
    print(v.size)
    time.sleep(2)
    v.close()
    time.sleep(1)