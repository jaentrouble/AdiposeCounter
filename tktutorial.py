import tkinter as tk
from tkinter import ttk

def calculate(*args):
    try :
        value = float(feet.get())
        meter.set((0.3048 * value * 10000 + 0.5)/10000)
    except ValueError:
        pass

root = tk.Tk()
root.title('Feet to meters')

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.config(borderwidth= 2, relief='sunken')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = tk.StringVar()
meter = tk.StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(tk.W,tk.E))

ttk.Label(mainframe, textvariable=meter).grid(column=2, row=2, sticky=(tk.W, tk.E))
ttk.Button(mainframe, text='Calculate', command=calculate).grid(column=3, row=3, sticky=tk.W)

ttk.Label(mainframe, text='feet').grid(column=3, row=1, stick=tk.W)
ttk.Label(mainframe, text='is eq. to').grid(column=1, row=2, sticky=tk.E)
ttk.Label(mainframe, text='meters').grid(column=3, row=2, sticky=tk.W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()