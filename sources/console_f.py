from .common.constants import *

## commands to call from console

# Functions for Top-left threshold setting menu ###############################
def button_mem_col_f(q):
    q.put({SET_MEM:None})

def button_cell_col_f(q):
    q.put({SET_CELL:None})

def button_ratio_f(ratio, q):
    print(ratio.get())
    q.put({SET_RATIO:ratio.get()})

# Functions for Top-Middle show/hide mask menu ################################
def button_show_mask_f(q):
    q.put({MODE_MASK:None})

def button_hide_mask_f(q):
    q.put({MODE_IMAGE:None})

# Functions for Top-Right Prev/Next menu ######################################
def button_prev_f():
    print('button_prev_f not implemented yet')

def button_next_f():
    print('button_next_f not implemented yet')

# Functions for Bottom-Left Draw menu #########################################
def button_draw_border_f():
    print('button_draw_border_f not implemented yet')

def button_draw_cell_f():
    print('button_draw_cell_f not implemented yet')

# Functions for Bottom-Middle Fill menu
def button_fill_cell_f():
    print('button_fill_cell_f not implemented yet')

# Functions for Bottom-Right Save menu
def button_save_f():
    print('button_save_f not implemented yet')

def button_delete_f():
    print('button_delete_f not implemented yet')