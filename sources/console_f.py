from .common.constants import *
from tkinter import messagebox

## commands to call from console

# Functions for Top-left threshold setting menu ###############################
def button_tf_set_f(q):
    q.put({SET_TF:None})

# def button_cell_col_f(q):
#     q.put({SET_CELL:None})

def button_ratio_f(ratio, q):
    print(ratio.get())
    answer = messagebox.askyesno(message='This will reset your mask.\
        \nContinue?')
    if answer:
        q.put({SET_RATIO:ratio.get()})

# Functions for Top-Middle show/hide mask menu ################################
def button_show_mask_f(q):
    q.put({MODE_MASK:None})

def button_hide_mask_f(q):
    q.put({MODE_IMAGE:None})

# Functions for Top-Right Prev/Next menu ######################################
# All functions are implemented in Console method
# def button_prev_f():
#     print('button_prev_f not implemented yet')

# def button_next_f():
#     print('button_next_f not implemented yet')

# button_open_f is implemented in Console method

# Functions for Bottom-Left Draw menu #########################################
# button_draw_cancel_f implemented in Console method

def button_draw_border_f(q):
    q.put({DRAW_MEM:None})

def button_draw_cell_f(q):
    q.put({DRAW_CELL:None})

def button_draw_apply_f(q):
    answer = messagebox.askyesno(message='Apply all drawings?')
    if answer:
        q.put({DRAW_OFF:None})

# Functions for Bottom-Middle Fill menu
def button_fill_ratio_f(q):
    q.put({FILL_MP_RATIO:None})

def button_fill_cell_f(q):
    answer = messagebox.askyesno(message='This will Apply all drawn layers\
        \nContinue?')
    if answer:
        q.put({FILL_CELL:None})

# Functions for Bottom-Right Save menu
# def button_save_f():
#     print('button_save_f not implemented yet')

# Implemented in Console method
# def button_delete_f():
#     print('button_delete_f not implemented yet')