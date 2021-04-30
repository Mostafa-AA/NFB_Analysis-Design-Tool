import Freq_Response as fr
import numpy as np
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk


def fn():
    blocks = ('A(s)', 'B(s)', 'C(s)')
    data = (('A', 'A', 'A', 'A'), ('B', 'B', 'B', 'B'), ('C', 'C', 'C', 'C'))
    i = 0
    x = table.get_children()

    for item in x:
        table.item(item, text=blocks[i], values=data[i])
        i = i + 1


def delete():
    selected_item = table.selection()[0]
    print(selected_item)
    table.delete(selected_item)


window1 = tk.ThemedTk()
window1.get_themes()
window1.set_theme('radiance')
window1.state('zoomed')

frame1 = ttk.Frame(window1)
frame1.pack()
table = ttk.Treeview(frame1)
table['columns'] = ('Poles', 'Zeros', 'Numerator Polynomial', 'Denominator Polynomial')
table.column('#0', width=60, minwidth=50)
table.column('Poles', width=100, minwidth=50, anchor=tkinter.CENTER)
table.column('Zeros', width=100, minwidth=50, anchor=tkinter.CENTER)
table.column('Numerator Polynomial', width=100, minwidth=50, anchor=tkinter.CENTER)
table.column('Denominator Polynomial', width=100, minwidth=50, anchor=tkinter.CENTER)
# ---------------------------------------------------------------------------------
table.heading('#0', text='Block')
table.heading('Poles', text='Poles', anchor=tkinter.CENTER)
table.heading('Zeros', text='Zeros', anchor=tkinter.CENTER)
table.heading('Numerator Polynomial', text='Numerator Polynomial', anchor=tkinter.CENTER)
table.heading('Denominator Polynomial', text='Denominator Polynomial', anchor=tkinter.CENTER)
# -------------------------------------------------------------------------------------------
table.insert('', 0, text='A(s)', values=('empty', 'empty', 'empty', 'empty'))
table.insert('', 1, text='B(s)', values=('empty', 'empty', 'empty', 'empty'))
table.insert('', 2, text='C(s)', values=('empty', 'empty', 'empty', 'empty'))
table.pack()

btn = ttk.Button(window1, text='Click', command=fn)
btn.pack()
btn = ttk.Button(window1, text='del', command=delete)
btn.pack()
L = ttk.Label(window1,text = 'S',font=('Arial',26))
L.pack()
window1.mainloop()
