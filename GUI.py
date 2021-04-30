import Freq_Response as fr
import numpy as np
import sys
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
window1 = tk.ThemedTk()
window1.get_themes()
window1.set_theme('adapta')

window1.state('zoomed')
window1.title("Negative Feedback Analysis Tool (Beta Version)")
window1.iconbitmap('logo.ico')
statusbar = ttk.Label(window1, text='>>Welcome to NFB Analysis Tool',relief=SUNKEN, anchor = W,font='Verdana 12 bold')
statusbar.pack(side=BOTTOM, fill=X)

left_frame = ttk.Frame(window1)
left_frame.pack(side=LEFT)
middle_frame = ttk.Frame(window1,width=500)
middle_frame.pack(side=TOP)
right_frame = ttk.Frame(window1,width=100)
right_frame.pack(side=RIGHT)
menubar = Menu(window1)
window1.config(menu=menubar)
submenu = Menu(menubar, tearoff=0)
file = menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label='New design')
submenu.add_command(label='Save')
submenu.add_command(label='Load')
submenu.add_command(label='Open')
submenu.add_command(label='Exit')
menubar.add_cascade(label="Edit", menu=submenu)
menubar.add_cascade(label="View", menu=submenu)
menubar.add_cascade(label="Run", menu=submenu)
menubar.add_cascade(label="Tools", menu=submenu)
menubar.add_cascade(label="Tabs", menu=submenu)
menubar.add_cascade(label="Help", menu=submenu)

NFB_block = PhotoImage(file='NFB_block.png')
labelphoto = ttk.Label(middle_frame, image=NFB_block)
labelphoto.pack()
run = PhotoImage(file='run_btn.png')
stop = PhotoImage(file='stop_btn.png')
reset = PhotoImage(file='reset_btn.png')
check = PhotoImage(file='check.png')
run_btn = ttk.Button(left_frame,image=run,stat=NORMAL)
run_btn.pack(pady=20)
stop_btn = ttk.Button(left_frame,image=stop,stat=NORMAL)
stop_btn.pack()
reset_btn = ttk.Button(left_frame,image=reset,stat=NORMAL)
reset_btn.pack()

lb = Listbox(window1)
lb.insert(0,'Transfer Function')
lb.insert(1,'Poles & Zeros')
lb.pack()
window1.mainloop()
