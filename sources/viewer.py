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
        self._show_cursor = False

    def run(self) :
        """
        Run viewer's mainloop
        """
        mainloop = True
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self._background = pygame.Surface(self.size)
        self._allgroup = pygame.sprite.LayeredDirty()
        self._cursor = Cursor()
        self._big_cursor = BigCursor()
        self._cross_cursor = CrossCursor()
        self._cursor.add(self._allgroup)
        self._big_cursor.add(self._allgroup)
        self._cross_cursor.add(self._allgroup)

        self._font = pygame.font.SysFont('Arial', 15)
        self._cell_areas = []

        self._mouse_prev = pygame.mouse.get_pos()
        while mainloop :
            self._clock.tick(self._fps)
            if not self._image_queue.empty():
                image = self._image_queue.get()
                if image.shape[0:2] != self.size:
                    self.size = image.shape[0:2]
                    self._screen = pygame.display.set_mode(self.size)
                    self._background = pygame.Surface(self.size)
                pygame.surfarray.blit_array(self._background, image)
                self._screen.blit(self._background, (0,0))
            if not self._etc_queue.empty():
                q = self._etc_queue.get()
                for k, v in q.items():
                    if k == TERMINATE:
                        mainloop=False
                    elif k == MOUSEPOS_ON:
                        self._put_mouse_pos = True
                    elif k == MOUSEPOS_OFF:
                        self._put_mouse_pos = False
                    elif k == BIG_CURSOR_ON:
                        self._big_cursor.visible = True
                        self._cursor.visible = False
                        # To erase it from the screen
                        self._cursor.dirty = True
                    elif k == BIG_CURSOR_OFF:
                        self._cursor.visible = True
                        self._big_cursor.visible = False
                        # To erase it from the screen
                        self._big_cursor.dirty = True
                    elif k == CROSS_CURSOR_ON:
                        self._cross_cursor.visible = True
                        self._cursor.visible = False
                        self._cursor.dirty = True
                    elif k == CROSS_CURSOR_OFF:
                        self._cursor.visible = True
                        self._cross_cursor.visible = False
                        self._cross_cursor.dirty = True

                    elif k == POS_LIST:
                        self.update_area(v)
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    # if event.key == pygame.K_ESCAPE :
                    #     mainloop = False 
            ######################################
            # Keyboard events
                    if event.key == pygame.K_z:
                        self._event_queue.put({K_Z:None})
                    elif event.key == pygame.K_RETURN:
                        self._event_queue.put({K_ENTER:None})
                    elif event.key == pygame.K_ESCAPE :
                        self._event_queue.put({K_ESCAPE:None})
                    elif event.key == pygame.K_b:
                        self._event_queue.put({K_B:None})
            # Mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self._event_queue.put({MOUSEDOWN:pygame.mouse.get_pos()})
                    elif pygame.mouse.get_pressed()[2]:
                        self._event_queue.put({MOUSEDOWN_RIGHT:pygame.mouse.get_pos()})
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._event_queue.put({MOUSEUP:None})

            if self._put_mouse_pos and self._mouse_prev!=pygame.mouse.get_pos():
                self._mouse_prev = pygame.mouse.get_pos()
                self._event_queue.put({MOUSEPOS:pygame.mouse.get_pos()})
            self._allgroup.update()
            self._allgroup.clear(self._screen, self._background)
            self._allgroup.draw(self._screen)
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

    def update_area(self, pos_list):
        idx = 0
        for idx, pa in enumerate(pos_list):
            pos, area = pa
            if idx >= len(self._cell_areas):
                new_cell = CellArea(self._font, area, pos)
                self._allgroup.add(new_cell)
                self._cell_areas.append(new_cell)
            else :
                self._cell_areas[idx].change_area(area, pos)
                self._cell_areas[idx].visible = True
                self._cell_areas[idx].dirty = True
        for ca in self._cell_areas[idx+1:]:
            ca.visible = False
            ca.dirty = True

    def close(self):
        pygame.quit()


class Cursor(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.image.fill(CURSOR)
        self.rect = self.image.get_rect()
        self.visible = True
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.dirty = 1

class BigCursor(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((11,11))
        self.image.fill(CURSOR)
        self.rect = self.image.get_rect()
        self.visible = False

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.dirty = 1

class CrossCursor(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        cursor_size = 100
        self.image = pygame.Surface((cursor_size*2,cursor_size*2))
        self.image.fill((0,0,0))
        pxarray = pygame.PixelArray(self.image)
        pxarray[:,cursor_size] = CURSOR
        pxarray[cursor_size,:] = CURSOR
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.visible = False

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.dirty = 1

class CellArea(pygame.sprite.DirtySprite):
    def __init__(self, Font, area, pos):
        """
        arguments
        ---------
        Font : pygame.font.Font
            Font object to render texts.
        area : float
            Text to show. Will convert to string anyway.
        pos : tuple
            (center_x,center_y)
        """
        super().__init__()
        self.font = Font
        self.area = area
        self.image = self.font.render(f'{area:.2f}', False,
                                (255,0,0), (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dirty = True

    def change_area(self, area, pos):
        if self.area != area:
            self.area = area
            self.image = self.font.render(f'{area:.2f}', False,
                                    (255,0,0), (255,255,255))
            self.dirty = True
        if (pos[0] != self.rect.centerx) or (pos[1] != self.rect.centery):
            self.rect.center = pos
            self.dirty = True


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