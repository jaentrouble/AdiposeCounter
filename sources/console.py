import tkinter as tk
from tkinter import ttk
from .console_f import *
from functools import partial
from PIL import ImageTk, Image
from multiprocessing import Process, Queue
from .common.constants import *
import os
from tkinter import filedialog, messagebox

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
        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self._list_items = []
        self._list_var = tk.DoubleVar(value=self._list_items)
        self.root.resizable(False, False)
        self._img_name_var = tk.StringVar(value='No image loaded')
        self._default_draw_mode_str = 'Click Buttons to draw'
        self._draw_mode_var = tk.StringVar(value=self._default_draw_mode_str)
        self._fill_ratio_var = tk.DoubleVar(value=DEFAULT_MP_RATIO)
        self._micro_var = tk.StringVar(value=DEFAULT_MP_MICRO)

        # Configure Top-left threshold setting menu ###########################
        self.frame_threshold = ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.frame_threshold.grid(column=0, row=0, sticky = (tk.W, tk.N))
        self.button_mem_col = ttk.Button(self.frame_threshold,
                                         text='Membrane Color',
                                         command=partial(button_mem_col_f,
                                         q=self._to_EngineQ))
        self.button_mem_col.grid(column=0, row=0, sticky=(tk.W))
        self.button_cell_col = ttk.Button(self.frame_threshold,
                                         text='Cell Color',
                                         command=partial(button_cell_col_f,
                                         q=self._to_EngineQ))
        self.button_cell_col.grid(column=0, row=1, sticky=(tk.W))
        ########### Color sample
        self.label_mem_color = ttk.Label(self.frame_threshold)
        self.image_mem_color = ImageTk.PhotoImage(Image.new('RGB', (30,30),
                                                            color=MEMBRANE
                                                            ))
        self.label_mem_color['image'] = self.image_mem_color
        self.label_mem_color.grid(column=1, row=0, sticky=(tk.W))
        ###
        self.label_cell_color = ttk.Label(self.frame_threshold)
        self.image_cell_color = ImageTk.PhotoImage(Image.new('RGB', (30,30),
                                                            color=CELL
                                                            ))
        self.label_cell_color['image'] = self.image_cell_color
        self.label_cell_color.grid(column=1, row=1, sticky=(tk.W))
        ###########
        self.ratio = tk.DoubleVar()
        self.scale_ratio = ttk.Scale(self.frame_threshold,
                                     from_=0, to=100, length=100,
                                     variable=self.ratio)
        self.scale_ratio.set(50)
        self.scale_ratio.grid(column=0, row=2)
        self.button_ratio = ttk.Button(self.frame_threshold,
                                       text='Set',
                                       command=partial(button_ratio_f, 
                                       self.ratio, self._to_EngineQ))
        self.button_ratio.grid(column=1, row=2)

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
        self.button_draw_cancel = ttk.Button(self.frame_draw,
                                             text='Cancel',
                                             command=self.button_draw_cancel_f)
        self.button_draw_cancel.grid(column=0, row=0)
        self.button_draw_border = ttk.Button(self.frame_draw,
                                             text='Draw Border',
                                             command=partial(button_draw_border_f,
                                             q=self._to_EngineQ))
        self.button_draw_border.grid(column=0, row=1)
        self.button_draw_cell = ttk.Button(self.frame_draw,
                                           text='Color White',
                                           command=partial(button_draw_cell_f,
                                           q=self._to_EngineQ))
        self.button_draw_cell.grid(column=0, row=2)
        self.button_draw_apply = ttk.Button(self.frame_draw,
                                            text='Apply',
                                            command=partial(button_draw_apply_f,
                                            q=self._to_EngineQ))
        self.button_draw_apply.grid(column=0, row=3)
        self.label_draw_mode = ttk.Label(self.frame_draw,
                                         textvariable=self._draw_mode_var)
        self.label_draw_mode.grid(column=1, row=0, rowspan=3)

        # Configure Bottom-Middle Fill menu ###################################
        self.frame_fill = ttk.Frame(self.root, padding='5 5 5 5')
        self.frame_fill.grid(column=1, row=1, sticky=(tk.W, tk.S))
        #TODO: Implement spinbox & Validate command
        self.label_fill_warning = ttk.Label(self.frame_fill,
                    text='Values : 1 ~ 1000')
        self.label_fill_warning.grid(column=0, row=0, columnspan=2)
        self.label_fill_micro = ttk.Label(self.frame_fill,
                                          text='Standard μm :')
        self.label_fill_micro.grid(column=0,row=1)
        self.spinbox_fill_micro = ttk.Spinbox(self.frame_fill,
                                              from_=1, to=1000,
                                              increment=5, width=5,
                                              textvariable=self._micro_var,
                                              command=self.spinbox_fill_micro_change)
        self.spinbox_fill_micro.bind('<Return>',self.spinbox_fill_micro_change)
        self.spinbox_fill_micro.grid(column=1, row=1)
        self.label_fill_ratio = ttk.Label(self.frame_fill,
                                         textvariable=self._fill_ratio_var)
        self.label_fill_ratio.grid(column=0, row=2)
        self.button_fill_ratio = ttk.Button(self.frame_fill,
                                            text='Set Length',
                                            command=partial(button_fill_ratio_f,
                                            q=self._to_EngineQ))
        self.button_fill_ratio.grid(column=0, row=3, sticky=(tk.N))
        self.button_fill_cell = ttk.Button(self.frame_fill,
                                           text='Fill Cell',
                                           command=partial(button_fill_cell_f,
                                           q=self._to_EngineQ))
        self.button_fill_cell.grid(column=0, row=4, sticky=(tk.S))
        
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
        self.button_save = ttk.Button(self.frame_save, text='Save',
                                      command=self.button_save_f)
        self.button_save.grid(column=2, row=1, sticky=(tk.E, tk.S))
        self.button_delete = ttk.Button(self.frame_save,
                                        text='Delete', command=self.button_delete_f)
        self.button_delete.grid(column=2, row=0, sticky=(tk.S))

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
    def mem_color(self):
        """Current color set for membrane"""
        return self._mem_color

    @mem_color.setter
    def mem_color(self, color):
        self._mem_color = color
        self.image_mem_color = ImageTk.PhotoImage(Image.new('RGB', (30,30),
                                                            color=self.mem_color
                                                            ))
        self.label_mem_color.configure(image=self.image_mem_color)

    @property
    def cell_color(self):
        """Current color set for cell"""
        return self._cell_color

    @cell_color.setter
    def cell_color(self, color):
        self._cell_color = color
        self.image_cell_color = ImageTk.PhotoImage(Image.new('RGB', (30,30),
                                                            color=self.cell_color
                                                            ))
        self.label_cell_color.configure(image=self.image_cell_color)

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
            for (dirpath, dirnames, filenames) in os.walk(self._image_folder):
                for f in filenames:
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
        self._to_EngineQ.put({FILL_MICRO:int(val)})

    def message_box(self, string):
        messagebox.showinfo(message=string)

    def update(self):
        if not self._to_ConsoleQ.empty():
            q = self._to_ConsoleQ.get()
            for k,v in q.items():
                if k == SET_MEM:
                    self.mem_color = tuple(v)
                elif k == SET_CELL:
                    self.cell_color = tuple(v)
                elif k == MODE_DRAW_MEM:
                    self._draw_mode_var.set('Draw membrane\nUndo:z\nStop:'\
                                'Right click\nPress Apply(Enter) when finished')
                elif k == MODE_DRAW_CELL:
                    self._draw_mode_var.set('Erase membrane\nUndo:z'
                        '\nPress Apply(Enter) when finished\n*Recommend applying every time')
                elif k == MODE_NONE:
                    self._draw_mode_var.set(self._default_draw_mode_str)
                elif k == MODE_FILL_CELL:
                    self._draw_mode_var.set('Click to fill a cell')
                elif k == MODE_FILL_MP_RATIO:
                    self._draw_mode_var.set('Set micrometer to pixel ratio')
                elif k == FILL_MP_RATIO:
                    self._fill_ratio_var.set(v)
                elif k == FILL_LIST:
                    self.list_items = v
                elif k == MESSAGE_BOX:
                    self.message_box(v)
        self.root.after(16, self.update)