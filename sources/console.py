import tkinter as tk
from tkinter import ttk
from .console_f import *
from functools import partial
from PIL import ImageTk, Image
from multiprocessing import Process, Queue
from .common.constants import *
import os
from tkinter import filedialog, messagebox
from . import iconarray
import numpy as np

class Console(Process):
    """
    Console
    All the commands called by buttons, etc. are in console_f.py
    """
    def __init__(self, to_ConsoleQ:Queue, to_EngineQ:Queue, termQ:Queue):
        """
        Tk objects are not pickleable
        Initiate all windows when start()
        """
        super().__init__(daemon=True)
        self._to_ConsoleQ = to_ConsoleQ
        self._to_EngineQ = to_EngineQ
        self._termQ = termQ
        self._image_name_list=[]

    def initiate(self):
        self.root = tk.Tk()
        self.root.title('Adipose Counter')

        array = np.array(iconarray.icon_array, dtype=np.uint8)
        icon_img = Image.fromarray(array)
        icon_tk = ImageTk.PhotoImage(icon_img)
        self.root.iconphoto(False, icon_tk)

        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self._list_items = []
        self._list_var = tk.DoubleVar(value=self._list_items)
        self.root.resizable(False, False)
        self._img_name_var = tk.StringVar(value='No image loaded')
        self._default_draw_mode_str = ''
        self._draw_mode_var = tk.StringVar(value=self._default_draw_mode_str)
        self._fill_ratio_var = tk.StringVar(
            value=f'{DEFAULT_MP_RATIO:.4f}μ㎡/pixel')
        self._micro_var = tk.StringVar(value=DEFAULT_MP_MICRO)
        self._pixel_var = tk.StringVar(value=DEFAULT_MP_PIXEL)

        # # Configure Top-left threshold setting menu ###########################
        self.frame_threshold = ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.frame_threshold.grid(column=0, row=0, sticky = (tk.W, tk.N))
        self.button_draw_box = ttk.Button(self.frame_threshold,
                                          text='Box',
                                          command=partial(button_draw_box_f,
                                          q=self._to_EngineQ))
        self.button_draw_box.grid(column=0, row=0, sticky=(tk.W))
        self.button_cancel_box = ttk.Button(self.frame_threshold,
                                          text='Cancel',
                                          command=partial(button_cancel_box_f,
                                          q=self._to_EngineQ))
        self.button_cancel_box.grid(column=0, row=1, sticky=(tk.W))

        self.ratio = tk.DoubleVar()
        self.scale_ratio = ttk.Scale(self.frame_threshold,
                                     from_=0, to=100, length=100,
                                     variable=self.ratio)
        self.scale_ratio.set(50)
        self.scale_ratio.grid(column=0, row=3)
        self.button_ratio = ttk.Button(self.frame_threshold,
                                       text='Set',
                                       command=partial(button_ratio_f, 
                                       self.ratio, self._to_EngineQ))
        self.button_ratio.grid(column=1, row=3)
        self.label_ratio = ttk.Label(self.frame_threshold,
                                     textvariable=self.ratio)
        self.label_ratio.grid(column=0, row=4)

        # Configure Top-Middle show/hide mask menu ############################
        self.frame_mask = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_mask.grid(column=1, row=0, sticky = (tk.W, tk.N, tk.E))
        self.button_show_mask = ttk.Button(self.frame_mask,
                                           text='Show mask',
                                           command=partial(button_show_mask_f,
                                           q=self._to_EngineQ))
        self.button_show_mask.grid(column=0, row=0)
        self.button_hide_mask = ttk.Button(self.frame_mask,
                                           text='Hide mask',
                                           command=partial(button_hide_mask_f,
                                           q=self._to_EngineQ))
        self.button_hide_mask.grid(column=0, row=1)

        # Configure Top-Right Prev/Next menu ##################################
        self.frame_prevnext = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_prevnext.grid(column=2, row=0, sticky = (tk.E, tk.N))
        self.button_prev = ttk.Button(self.frame_prevnext,
                                      text='Prev',
                                      command=self.button_prev_f)
        self.button_prev.grid(column=0, row=0)
        self.button_next = ttk.Button(self.frame_prevnext,
                                      text='Next',
                                      command=self.button_next_f)
        self.button_next.grid(column=0, row=1)
        self.button_open = ttk.Button(self.frame_prevnext,
                                      text='Open',
                                      command=self.button_open_f)
        self.button_open.grid(column=0, row=2)
        self.label_img_name = ttk.Label(self.frame_prevnext,
                                        textvariable=self._img_name_var)
        self.label_img_name.grid(column=0, row=3)

        # Configure Bottom-Left Draw menu #####################################
        self.frame_draw = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_draw.grid(column=0, row=1, sticky=(tk.W, tk.S))
        self.label_draw_mode = ttk.Label(self.frame_draw,
                                         textvariable=self._draw_mode_var)
        self.label_draw_mode.grid(column=0, row=0)

        # Configure Bottom-Middle Fill menu ###################################
        self.frame_fill = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_fill.grid(column=1, row=1, sticky=(tk.W, tk.S))
        # self.label_fill_warning = ttk.Label(self.frame_fill,
        #             text='Values : 1 ~ 1000')
        # self.label_fill_warning.grid(column=0, row=0, columnspan=2)
        self.label_fill_micro = ttk.Label(self.frame_fill,
                                          text='Reference μm (1~1000) :',
                                          anchor='ne')
        self.label_fill_micro.grid(column=0,row=0, sticky=(tk.E))
        self.spinbox_fill_micro = ttk.Spinbox(self.frame_fill,
                                              from_=1, to=1000,
                                              increment=5, width=5,
                                              textvariable=self._micro_var,
                                              command=self.spinbox_fill_micro_change)
        self.spinbox_fill_micro.bind('<Return>',self.spinbox_fill_micro_change)
        self.spinbox_fill_micro.grid(column=1, row=0, sticky=(tk.NW))
        self.label_fill_pixel = ttk.Label(self.frame_fill,
                                          text='Reference pixel(Original image) :')
        self.label_fill_pixel.grid(column=0,row=1)
        self.entry_fill_pixel = ttk.Entry(self.frame_fill,
                                          textvariable=self._pixel_var,
                                          width=10)
        self.entry_fill_pixel.bind('<Return>',self.entry_fill_pixel_change)
        self.entry_fill_pixel.grid(column=1,row=1)
        self.button_fill_pixel_set = ttk.Button(self.frame_fill,
                                                text='Set pixel',
                                                command=self.entry_fill_pixel_change)
        self.button_fill_pixel_set.grid(column=2, row=1)
        self.label_fill_ratio = ttk.Label(self.frame_fill,
                                         textvariable=self._fill_ratio_var)
        self.label_fill_ratio.grid(column=0, row=2)
        self.button_fill_ratio = ttk.Button(self.frame_fill,
                                            text='Manually set ratio',
                                            command=partial(button_fill_ratio_f,
                                            q=self._to_EngineQ))
        self.button_fill_ratio.grid(column=0, row=3, sticky=(tk.N))
        
        # Configure Bottom-Right Save menu ####################################
        self.frame_save = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_save.grid(column=2, row=1, sticky=(tk.E, tk.S))
        self.list_save = tk.Listbox(self.frame_save, height=15,
                                    listvariable=self._list_var)
        self.list_save.grid(column=0, row=0, sticky=(tk.E, tk.N))
        self.scroll_save = ttk.Scrollbar(self.frame_save,
                                         command=self.list_save.yview)
        self.scroll_save.grid(column=1, row=0, sticky=(tk.E, tk.N, tk.S))
        self.list_save.configure(yscrollcommand=self.scroll_save.set)
        self.button_delete = ttk.Button(self.frame_save,
                                        text='Delete', command=self.button_delete_f)
        self.button_delete.grid(column=2, row=0, sticky=(tk.S))
        self.button_save = ttk.Button(self.frame_save, text='Save',
                                      command=self.button_save_f)
        self.button_save.grid(column=2, row=1, sticky=(tk.E, tk.S))

        # Set weights of frames ###############################################
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)


    def run(self):
        self.initiate()
        self.button_open_f(ask=False)
        self.root.after(16, self.update)
        self.root.mainloop()
        self._termQ.put(TERMINATE)



    @property
    def list_items(self):
        """
        Items currently in the list.
        Should be list of floats
        """
        return self._list_items.copy()

    @list_items.setter
    def list_items(self, list_of_items):
        self._list_items = list_of_items.copy()
        self._list_var.set(self._list_items)

    def button_open_f(self, ask=True):
        if ask:
            answer = messagebox.askyesno(message='This will reset everything.'\
                                                '\n Continue?')
            if not answer: return
        dirname = filedialog.askdirectory()
        if dirname == '':
            pass
        else:
            self._image_folder = dirname
            self._image_name_list = []
            self._image_idx = 0
            for f in os.listdir(self._image_folder):
                if f.endswith(IMAGE_FORMATS):
                    self._image_name_list.append(f)
            self._to_EngineQ.put({
                NEWIMAGE:os.path.join(self._image_folder,
                        self._image_name_list[self._image_idx])
            })
            self._img_name_var.set(self._image_name_list[self._image_idx])

    def button_next_f(self):
        answer = messagebox.askyesno(message='All unsaved values will disappear.\
            \nContinue?')
        if answer:
            if len(self._image_name_list) > 0 :
                self._image_idx = (self._image_idx+1)%len(self._image_name_list)
                self._to_EngineQ.put({
                    NEWIMAGE:os.path.join(self._image_folder,
                            self._image_name_list[self._image_idx])
                })
                self._img_name_var.set(self._image_name_list[self._image_idx])

    def button_prev_f(self):
        answer = messagebox.askyesno(message='All unsaved values will disappear.\
            \nContinue?')
        if answer:
            if len(self._image_name_list) > 0 :
                self._image_idx = (self._image_idx-1)%len(self._image_name_list)
                self._to_EngineQ.put({
                    NEWIMAGE:os.path.join(self._image_folder,
                            self._image_name_list[self._image_idx])
                })
                self._img_name_var.set(self._image_name_list[self._image_idx])

    def button_draw_cancel_f(self):
        answer = messagebox.askyesno(message='This will delete all unapplied drawings.\
            \nContinue?')
        if answer:
            self._to_EngineQ.put({DRAW_CANCEL:None})

    def button_delete_f(self):
        answer = messagebox.askyesno(message='Delete selected Cell?')
        if answer:
            self._to_EngineQ.put({FILL_DELETE:self.list_save.curselection()})

    def button_save_f(self):
        save_dir = filedialog.askopenfilename(title='Select Excel File',
                    filetypes=[('Excel files','*.xlsx')])
        if save_dir == '':
            pass
        else:
            self._to_EngineQ.put({FILL_SAVE:(save_dir, 
                                self._image_name_list[self._image_idx],
                                self._image_folder)})

    def spinbox_fill_micro_change(self, *args):
        val = self._micro_var.get()
        if val.isdigit():
            if int(val)>1000:
                self._micro_var.set(1000)
                val = 1000
            elif int(val)<1:
                self._micro_var.set(1)
                val = 1
        else :
            self._micro_var.set(DEFAULT_MP_MICRO)
            val = DEFAULT_MP_MICRO
            self.message_box('Only positive numbers are allowed')
        self._to_EngineQ.put({FILL_MICRO:int(val)})

    def entry_fill_pixel_change(self, *args):
        val = self._pixel_var.get()
        try:
            pixel = float(val)
            if pixel<=0:
                raise ValueError
        except ValueError:
            self._pixel_var.set(DEFAULT_MP_PIXEL)
            pixel = DEFAULT_MP_PIXEL
            self.message_box('Only positive numbers are allowed')
        self._to_EngineQ.put({FILL_PIXEL:pixel})

    def message_box(self, string):
        messagebox.showinfo(message=string)

    def update(self):
        if not self._to_ConsoleQ.empty():
            q = self._to_ConsoleQ.get()
            for k,v in q.items():
                if k == MODE_NONE:
                    self._draw_mode_var.set(self._default_draw_mode_str)
                elif k == MODE_FILL_MP_RATIO:
                    self._draw_mode_var.set('Set micrometer to pixel ratio')
                elif k == FILL_MP_RATIO:
                    self._fill_ratio_var.set(f'{v:.4f}μ㎡/pixel')
                elif k == FILL_LIST:
                    self.list_items = v
                elif k == FILL_PIXEL:
                    self._pixel_var.set(v)
                elif k == MESSAGE_BOX:
                    self.message_box(v)
        self.root.after(16, self.update)