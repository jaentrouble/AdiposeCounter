import numpy as np
from multiprocessing import Process, Queue
from PIL import Image
from .common.constants import *
from skimage import draw

# To limit loop rate
from pygame.time import Clock

class Engine(Process):
    """
    Main process that calculates all the necessary computations
    """
    # If the image is not updated, check if self._updated is switched to True
    def __init__(self, to_EngineQ:Queue, to_ConsoleQ:Queue,
                 imageQ:Queue, eventQ:Queue, etcQ:Queue):
        super().__init__(daemon=True)
        self.image = np.zeros((300,300,3), dtype=np.uint8)
        self.set_empty_mask()
        self._to_EngineQ = to_EngineQ
        self._to_ConsoleQ = to_ConsoleQ
        self._imageQ = imageQ
        self._eventQ = eventQ
        self._etcQ = etcQ
        self._mask_mode = False
        self._updated = True
        self._color_mode = None
        self.mem_color = MEMBRANE
        self.cell_color = CELL
        self._layers = []
        self._draw_mode = None
        self._is_drawing = False

    @property
    def image(self):
        """
        This is a base image. Do not directly modify this
        """
        return self._image.copy()

    @image.setter
    def image(self, image:np.array):
        """
        Must be a shape of (width, height, 3)
        """
        if len(image.shape) != 3 and image.shape[2] != 3:
            raise TypeError('Inappropriate shape of image')
        self._image = image.astype(np.uint8)

    @property
    def mask(self):
        """
        This is the mask on which engine computes
        """
        return self._mask

    @mask.setter
    def mask(self, mask:np.array):
        """
        Must be a shape of (width, height, 3) and same as current image
        """
        if mask.shape != self.image.shape:
            raise TypeError('Inappropriate shape of mask')
        self._mask = mask.astype(np.uint8)

    @property
    def cell_color(self):
        return self._cell_color

    @cell_color.setter
    def cell_color(self, color):
        if len(color) != 3 :
            raise TypeError('Wrong color given')
        self._cell_color = color

    @property
    def mem_color(self):
        return self._mem_color

    @mem_color.setter
    def mem_color(self, color):
        if len(color) != 3 :
            raise TypeError('Wrong color given')
        self._mem_color = color

    @property
    def mask_mode(self):
        return self._mask_mode

    @mask_mode.setter
    def mask_mode(self, mask_mode:bool):
        self._mask_mode = mask_mode
        self._updated = True

    def load_image(self, path:str):
        #TODO: Resize image?
        im = Image.open(path)
        self.image = np.asarray(im).swapaxes(0,1)
        self._updated = True

    def set_empty_mask(self):
        """
        Set a new empty mask that is the same shape as current image
        """
        self.mask = np.zeros_like(self.image)
        self._updated = True

    def set_new_mask(self, ratio:float):
        """
        ratio : if ratio * dist_to_memcolor > (1-ratio) * dist_to_cellcolor,
        the pixel is considered as cell
        """
        print('set new mask')
        ratio /=100
        dist_to_memcolor=((self.image.astype(np.int) - self.mem_color)**2).sum(
                                                        axis=2,
                                                        keepdims=True)
        dist_to_cellcolor=((self.image.astype(np.int) - self.cell_color)**2).sum(
                                                        axis=2,
                                                        keepdims=True)
        print(ratio)
        self._mask_bool = (dist_to_memcolor*ratio) > (dist_to_cellcolor*(1-ratio))
        self.mask = self._mask_bool * CELL
        self._updated = True
    
    def put_image(self):
        if self._mask_mode:
            self._imageQ.put(self.mask)
        else:
            self._imageQ.put(self.image)

    def draw_mem_start(self, pos):
        #TODO:implement
        pass

    def run(self):
        mainloop = True
        self._clock = Clock()
        while mainloop:
            self._clock.tick(60)
            if not self._to_EngineQ.empty():
                q = self._to_EngineQ.get()
                for k, v in q.items():
                    if k == NEWIMAGE:
                        self.load_image(v)
                    elif k == NEWMASK:
                        self.set_new_mask(*v)
                    elif k == MODE_IMAGE:
                        self.mask_mode = False
                    elif k == MODE_MASK:
                        self.mask_mode = True
                    elif k == TERMINATE:
                        mainloop = False
                    elif k == SET_MEM:
                        self._color_mode = SET_MEM
                    elif k == SET_CELL:
                        self._color_mode = SET_CELL
                    elif k == SET_RATIO:
                        self.set_new_mask(v)
                    elif k == DRAW_MEM:
                        self._draw_mode = DRAW_MEM

            if not self._eventQ.empty():
                q = self._eventQ.get()
                for k,v in q.items():
                    if k == MOUSEDOWN:
                        print(self._color_mode)
                        if self._color_mode == SET_MEM:
                            self.mem_color = self.image[v]
                            print(self.mem_color)
                            self._color_mode = None
                            self._to_ConsoleQ.put({SET_MEM:self.mem_color})
                        elif self._color_mode == SET_CELL:
                            self.cell_color = self.image[v]
                            self._color_mode = None
                            print(self.cell_color)
                            self._to_ConsoleQ.put({SET_CELL:self.cell_color})

            if self._updated:
                self.put_image()
                self._updated = False