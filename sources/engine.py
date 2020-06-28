import numpy as np
from multiprocessing import Process, Queue
from PIL import Image
from .common.constants import *
from skimage import draw, transform

# To limit loop rate
from pygame.time import Clock

# TODO: make undo


class Engine(Process):
    """
    Main process that calculates all the necessary computations
    """
    # If the image is not updated, check if self._updated is switched to True
    def __init__(self, to_EngineQ:Queue, to_ConsoleQ:Queue,
                 imageQ:Queue, eventQ:Queue, etcQ:Queue):
        super().__init__(daemon=True)
        # Initial image and mask
        self.image = np.zeros((300,300,3), dtype=np.uint8)
        self.set_empty_mask()
        # Queues
        self._to_EngineQ = to_EngineQ
        self._to_ConsoleQ = to_ConsoleQ
        self._imageQ = imageQ
        self._eventQ = eventQ
        self._etcQ = etcQ
        # Modes about sending images to Viewer
        self._mask_mode = False
        self._updated = True
        # Do only one thing at a time - Do not make multiple modes
        self._mode = None
        # Initial membrane and cell color (NOT MASK COLORS)
        self.mem_color = MEMBRANE
        self.cell_color = CELL
        # (Color_of_layer(R,G,B), Bool mask(Width, Height, 1))
        #TODO: Use different list for cell count layers to prevent merging with
        #      Cell-Membrane layers
        self._layers = []
        # Modes related to drawings
        self._is_drawing = False
        self._line_start_pos = None

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
        return self._mask.copy()

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
        self.image = transform.resize(np.asarray(im).swapaxes(0,1),(800,600))*255
        self.set_empty_mask()
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
            tmp_mask = self.mask
            for c, m in self._layers:
                np.multiply(tmp_mask, np.logical_not(m), out=tmp_mask)
                np.add(tmp_mask, m * np.array(c,np.uint8), out=tmp_mask)
            self._imageQ.put(tmp_mask)
        else:
            self._imageQ.put(self.image)

    def put_mode(self):
        if self._mode != None:
            self._to_ConsoleQ.put({self._mode:None})
        else:
            self._to_ConsoleQ.put({MODE_NONE:None})

    def draw_mem_start(self, pos):
        """
        Make a new layer and draw inital point (Red dot)
        """
        new_layer = np.zeros((self.mask.shape[0],self.mask.shape[1],1),
                             dtype=np.bool)
        color = LINE_START
        x, y = pos
        new_layer[x:x+3, y:y+3] = True
        self._layers.append((color, new_layer))
        self._line_start_pos = pos
        self._is_drawing = True
        self._updated = True

    def draw_mem_end(self, pos):
        """
        Draw the line and start next line
        """
        _, last_layer = self._layers.pop()
        new_layer = np.zeros_like(last_layer)
        color = MEMBRANE
        del last_layer
        r0, c0 = self._line_start_pos
        r1, c1 = pos
        rr, cc, _ = draw.line_aa(r0, c0, r1, c1)
        new_layer[rr, cc] = True
        self._layers.append((color, new_layer))
        self._line_start_pos = None
        # self._is_drawing = False
        self.draw_mem_start(pos)
        self._updated = True
        
    def draw_stop(self):
        """
        Stop connecting lines; Similar to draw_undo
        """
        if self._is_drawing :
            self._layers.pop()
            self._is_drawing = False
            self._line_start_pos = None
            self._updated=True

    def draw_apply(self):
        if self._is_drawing:
            self.draw_stop()
        tmp_mask = self.mask
        for c, m in self._layers:
            np.multiply(tmp_mask, np.logical_not(m), out=tmp_mask)
            np.add(tmp_mask, m * np.array(c,np.uint8), out=tmp_mask)
        self._layers = []
        self.mask = tmp_mask
        self._updated = True
        self._mode = None

    def draw_undo(self):
        if len(self._layers)>0 :
            self._layers.pop()
            self._is_drawing = False
            self._line_start_pos = None
            self._updated = True

    def draw_cancel(self):
        self._layers = []
        self._is_drawing = False
        self._line_start_pos = None
        self._mode = None
        self._updated = True

    def run(self):
        mainloop = True
        self._clock = Clock()
        while mainloop:
            self._clock.tick(60)
            if not self._to_EngineQ.empty():
                q = self._to_EngineQ.get()
                for k, v in q.items():
                    if k == TERMINATE:
                        mainloop = False
                    # Loading & Showing modes
                    elif k == NEWIMAGE:
                        self.load_image(v)
                    elif k == NEWMASK:
                        self.set_new_mask(*v)
                    elif k == MODE_IMAGE:
                        self.mask_mode = False
                    elif k == MODE_MASK:
                        self.mask_mode = True
                    # Set colors & ratio
                    elif k == SET_MEM:
                        self._mode = MODE_SET_MEM
                    elif k == SET_CELL:
                        self._mode = MODE_SET_CELL
                    elif k == SET_RATIO:
                        self.set_new_mask(v)
                    #Drawing modes
                    elif k == DRAW_MEM:
                        self._mode = MODE_DRAW_MEM
                        self._updated = True
                    elif k == DRAW_CELL:
                        #TODO: implement draw_cell
                        pass
                    elif k == DRAW_OFF:
                        self.draw_apply()
                    elif k == DRAW_CANCEL:
                        self.draw_cancel()

            if not self._eventQ.empty():
                q = self._eventQ.get()
                for k,v in q.items():
                    if k == MOUSEDOWN:
                        # v : mouse pos which came from Viewer
                        # Set color
                        print('clicked')
                        if self._mode == MODE_SET_MEM:
                            self.mem_color = self.image[v]
                            print(self.mem_color)
                            self._color_mode = None
                            self._to_ConsoleQ.put({SET_MEM:self.mem_color})
                        elif self._mode == MODE_SET_CELL:
                            self.cell_color = self.image[v]
                            self._color_mode = None
                            print(self.cell_color)
                            self._to_ConsoleQ.put({SET_CELL:self.cell_color})
                        # Drawing mode
                        elif self._mode == MODE_DRAW_MEM and not self._is_drawing:
                            self.draw_mem_start(v)
                        elif self._mode == MODE_DRAW_MEM and self._is_drawing:
                            self.draw_mem_end(v)
                    # Keyboard events
                    elif k == K_Z:
                        self.draw_undo()
                    elif k == K_ENTER:
                        self.draw_stop()

            if self._updated:
                self.put_image()
                self.put_mode()
                self._updated = False