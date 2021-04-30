import Freq_Response as fr
import numpy as np
import sys
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog



def print_hello():
    statusbar['text'] = '>>hello!'


def value(val):
    statusbar['text'] = '>>'+str(val)
    b3['state'] = NORMAL


def new_design():
    statusbar['text'] = 'new design'


def exit_():
    if tkinter.messagebox.askokcancel('Negative Feedback Analysis Tool', 'Are you sure want to exit?'):
        statusbar['text'] = 'exit'
        window.destroy()


def browse_file():
    global filename
    filename = filedialog.askopenfilename()




window = Tk()

liftframe = Frame(window, relief=RAISED,borderwidth=1)
liftframe.pack(padx = 50,pady = 100)

menubar = Menu(window)
window.config(menu=menubar)
submenu = Menu(menubar, tearoff=0)
file = menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label='New design', command=new_design)
submenu.add_command(label='Save')
submenu.add_command(label='Load')
submenu.add_command(label='Open', command=browse_file)
submenu.add_command(label='Exit', command=exit_)
menubar.add_cascade(label="Edit", menu=submenu)
menubar.add_cascade(label="View", menu=submenu)
menubar.add_cascade(label="Run", menu=submenu)
menubar.add_cascade(label="Tools", menu=submenu)
menubar.add_cascade(label="Tabs", menu=submenu)
menubar.add_cascade(label="Help", menu=submenu)

w, h = window.winfo_screenwidth(), window.winfo_screenheight()
# window.geometry("%dx%d+0+0" % (w, h))
# window.attributes("-fullscreen", False)
window.state('zoomed')
window.title("Negative Feedback Analysis Tool (Beta Version)")
window.iconbitmap('logo.ico')
# b1 = Button(text='check', stat=DISABLED).pack(pady=50)
# b1 = Button(text='check', stat=DISABLED).pack(pady=50)
# b1 = Button(text='check', stat=DISABLED).pack(pady=50)
# b1 = Button(text='check', stat=DISABLED).pack(pady=50)
# b2 = Button(text='check', stat=DISABLED).place(x=100,y=200)
print()
# l1 = Label(text = 'check',fg = 'blue', bg = 'green').pack()
photo = PhotoImage(file='NFB_block.png')
labelphoto = Label(liftframe, image=photo)
labelphoto.pack(side = LEFT,padx = 10,pady=10)
k = 1000
b3 = Button(liftframe,image=photo, command=print_hello, stat=DISABLED)
b3.pack(side=LEFT,padx = 10,pady = 10)
sc = Scale(window, from_=0, to=k, orient=HORIZONTAL, command=value)
sc.set(0)
sc.pack()
statusbar = Label(window, text='>>Welcome to NFB Analysis Tool',relief=SUNKEN, anchor = W)
statusbar.pack(side=BOTTOM, fill=X)



window.mainloop()




















'''
a = fn.get_TF([], [-1000, -100],10000000)
beta = fn.get_TF([],[-1000000],1)
freq_range = fn.generate_freq(1,100000,1)

corn_freq = fn.get_CornerFreq(a,freq_range)
print(corn_freq)
#print(fn.BPF_QualityFactor(a,freq_range))
print(fn.BandWidth_LPF(a,freq_range))
print(fn.LoopGain(a,beta))
print(fn.get_data(a, freq_range,'mag',0))
print(fn.phase_margin_deg(a,freq_range))
print(fn.gain_margin_dB(a,freq_range))
print(fn.UnityGainFreq_rad(a,freq_range))
fn.BodePlot(a,freq_range,1)


print(fn.ClosedLoop_TF(a,beta))
zeros__,poles__ = fn.get_PZ(a)
print(zeros__)
print(poles__)
print(fn.DC_gain_dB(a))
print(fn.BandWidth_LPF(a))
fn.BodePlot(a)
fn.BodePlot(fn.ClosedLoop_TF(a,beta))
x = np.array([1,2,4])
y = np.polymul(np.array([1,2]),np.array([3,4]))
print(y)'''
