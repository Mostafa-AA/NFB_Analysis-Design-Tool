import Freq_Response as fr
import numpy as np
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter.ttk import *

# ----------functions----------
def check_fn():
    try:
        num_A = []
        den_A = []
        num_B = []
        den_B = []
        num_C = []
        den_C = []
        p_A = []
        z_A = []
        p_B = []
        z_B = []
        p_C = []
        z_C = []
        const_A, const_B, const_C = 0, 0, 0
        if flag_tf0_pz1_A == 0:
            num_A = fr.str2num(fr.str2arr(str(str_num_A)), 0)
            den_A = fr.str2num(fr.str2arr(str(str_den_A)), 0)
            A = 1
        elif flag_tf0_pz1_A == 1:
            p_A = fr.str2num(fr.str2arr(str(str_poles_A)), 1)
            z_A = fr.str2num(fr.str2arr(str(str_zeros_A)), 1)
            const_A = fr.str1_2_num(str(str_const_A))
            A = 1
        else:
            status_bar['text'] = '>>Empty inputs of A'
            A = 0

        if flag_tf0_pz1_B == 0:
            num_B = fr.str2num(fr.str2arr(str_num_B), 0)
            den_B = fr.str2num(fr.str2arr(str_den_B), 0)
            B = 1
        elif flag_tf0_pz1_B == 1:
            p_B = fr.str2num(fr.str2arr(str_poles_B), 1)
            z_B = fr.str2num(fr.str2arr(str_zeros_B), 1)
            const_B = fr.str1_2_num(str(str_const_B))
            B = 1
        else:
            status_bar['text'] = '>>Empty inputs of B'
            B = 0

        if flag_tf0_pz1_C == 0:
            num_C = fr.str2num(fr.str2arr(str_num_C), 0)
            den_C = fr.str2num(fr.str2arr(str_den_C), 0)
            C = 1
        elif flag_tf0_pz1_C == 1:
            p_C = fr.str2num(fr.str2arr(str_poles_C), 1)
            z_C = fr.str2num(fr.str2arr(str_zeros_C), 1)
            const_C = fr.str1_2_num(str(str_const_C))
            C = 1
        else:
            status_bar['text'] = '>>Empty inputs of C'
            C = 0
        if A == 1 and B == 1 and C == 1:
            run_btn['state'] = NORMAL
            status_bar['text'] = '>>Ready to run'
            # -------print out inputs--------------
            global data
            data = fr.create_data(num_A, den_A, num_B, den_B, num_C, den_C, p_A, z_A, p_B, z_B, p_C, z_C,
                                  flag_tf0_pz1_A, flag_tf0_pz1_B, flag_tf0_pz1_C, const_A, const_B, const_C)
            data1 = data + [('-', '-', '-', '-'), ('-', '-', '-', '-')]
            fill_table(data1)
            global inputs
            inputs = [num_A, den_A, z_A, p_A, const_A, num_B, den_B, z_B, p_B, const_B, num_C, den_C, z_C, p_C, const_C]
    except:
        reset_fn()
        status_bar['text'] = '>>Error, Check your inputs'
        run_btn['state'] = DISABLED


def run_fn():
    status_bar['text'] = '>>Loading.'
    TF_A, TF_B, TF_C = (), (), ()
    if flag_tf0_pz1_A == 0:
        TF_A = fr.num_den_TF(inputs[0], inputs[1], 1)
    elif flag_tf0_pz1_A == 1:
        TF_A, num_A, den_A = fr.get_TF(inputs[2], inputs[3], inputs[4])
    if flag_tf0_pz1_B == 0:
        TF_B = fr.num_den_TF(inputs[5], inputs[6], 1)
    elif flag_tf0_pz1_B == 1:
        TF_B, num_B, den_B = fr.get_TF(inputs[7], inputs[8], inputs[9])
    if flag_tf0_pz1_C == 0:
        TF_C = fr.num_den_TF(inputs[10], inputs[11], 1)
    elif flag_tf0_pz1_C == 1:
        TF_C, num_C, den_C = fr.get_TF(inputs[12], inputs[13], inputs[14])

    CL_s, num_cl, den_cl = fr.ClosedLoop_TF(TF_A, TF_B, TF_C)
    LG_s, num_lg, den_lg = fr.LoopGain(TF_A, TF_B)
    # -----------------------------------------------------------------------
    poles_cl, zeros_cl, n_cl, d_cl = fr.generate_num_den_pz(CL_s, num_cl, den_cl)
    poles_lg, zeros_lg, n_lg, d_lg = fr.generate_num_den_pz(LG_s, num_lg, den_lg)
    a = [(poles_lg, zeros_lg, n_lg, d_lg), (poles_cl, zeros_cl, n_cl, d_cl)]
    data1 = data + a
    fill_table(data1)
    status_bar['text'] = '>>Loading..'

    # -----------------------------------------------------------------------


def fill_table(data_):
    blocks = ('A(s)', 'B(s)', 'C(s)', 'LG(s)', 'CL(s)')
    i = 0
    x = table.get_children()

    for item in x:
        table.item(item, text=blocks[i], values=data_[i])
        i = i + 1


def reset_fn():  # note: must be modified after adding any object to window
    global str_poles_A
    global str_zeros_A
    global str_den_A
    global str_num_A
    global str_poles_B
    global str_zeros_B
    global str_den_B
    global str_num_B
    global str_poles_C
    global str_zeros_C
    global str_den_C
    global str_num_C
    global flag_tf0_pz1_A
    global flag_tf0_pz1_B
    global flag_tf0_pz1_C
    str_poles_A = ''
    str_zeros_A = ''
    str_num_A = ''
    str_den_A = ''
    str_poles_B = ''
    str_zeros_B = ''
    str_num_B = ''
    str_den_B = ''
    str_num_C = ''
    str_den_C = ''
    flag_tf0_pz1_A = -1
    flag_tf0_pz1_B = -1
    flag_tf0_pz1_C = -1
    A_btn['state'] = NORMAL
    B_btn['state'] = NORMAL
    C_btn['state'] = NORMAL
    run_btn['state'] = DISABLED
    status_bar['text'] = '>>Welcome To NFB Analysis Tool'
    x = table.get_children()
    for item in x:
        table.delete(item)
    table.insert('', 0, text='A(s)', values=('-', '-', '-', '-'))
    table.insert('', 1, text='B(s)', values=('-', '-', '-', '-'))
    table.insert('', 2, text='C(s)', values=('-', '-', '-', '-'))
    table.insert('', 3, text='LG(s)', values=('-', '-', '-', '-'))
    table.insert('', 4, text='CL(s)', values=('-', '-', '-', '-'))
    table.column('#0', width=60, minwidth=50)
    table.column('Poles', width=110, minwidth=50, anchor=tkinter.CENTER)
    table.column('Zeros', width=110, minwidth=50, anchor=tkinter.CENTER)
    table.column('Numerator Polynomial', width=158, minwidth=50, anchor=tkinter.CENTER)
    table.column('Denominator Polynomial', width=158, minwidth=50, anchor=tkinter.CENTER)


def exit_fn():
    status_bar['text'] = '>>Exit'
    if tkinter.messagebox.askokcancel('Negative Feedback Analysis Tool', 'Are you sure want to exit?'):
        window1.destroy()
    else:
        status_bar['text'] = '>>Welcome to NFB Analysis Tool'


def get_A():
    global str_poles_A
    global str_zeros_A
    global str_den_A
    global str_num_A
    global str_const_A

    def input_pz():
        clear_btn_tf()
        poles_textbox['state'] = NORMAL
        zeros_textbox['state'] = NORMAL
        const_textbox['state'] = NORMAL
        enter_pz_btn['state'] = NORMAL
        clear_pz_btn['state'] = NORMAL
        n_textbox['state'] = DISABLED
        d_textbox['state'] = DISABLED
        enter_tf_btn['state'] = DISABLED
        clear_tf_btn['state'] = DISABLED
        poles_textbox.insert(10, 'P1 P2 P3 ....')
        zeros_textbox.insert(10, 'Z1 Z2 Z3 ....')
        global flag_tf0_pz1_A
        flag_tf0_pz1_A = 1

    def input_tf():
        clear_btn()
        poles_textbox['state'] = DISABLED
        zeros_textbox['state'] = DISABLED
        const_textbox['state'] = DISABLED
        enter_pz_btn['state'] = DISABLED
        clear_pz_btn['state'] = DISABLED
        n_textbox['state'] = NORMAL
        d_textbox['state'] = NORMAL
        enter_tf_btn['state'] = NORMAL
        clear_tf_btn['state'] = NORMAL
        n_textbox.insert(10, 'coeff of (s^n ....... s^2 s^1 s^0)')
        d_textbox.insert(10, 'coeff of (s^n ....... s^2 s^1 s^0)')
        global flag_tf0_pz1_A
        flag_tf0_pz1_A = 0

    def enter_btn():
        global str_poles_A
        str_poles_A = poles_textbox.get()
        global str_zeros_A
        str_zeros_A = zeros_textbox.get()
        global str_const_A
        str_const_A = const_textbox.get()
        ok_btn['state'] = NORMAL

    def enter_btn_tf():
        global str_num_A
        str_num_A = n_textbox.get()
        global str_den_A
        str_den_A = d_textbox.get()
        ok_btn['state'] = NORMAL

    def clear_btn():
        zeros_textbox.delete(0, 100)
        poles_textbox.delete(0, 100)
        const_textbox.delete(0, 100)

    def clear_btn_tf():
        n_textbox.delete(0, 100)
        d_textbox.delete(0, 100)

    def ok_fn():
        status_bar['text'] = '>>Welcome To NFB Analysis Tool'
        window_A.destroy()

    window_A = tk.ThemedTk()
    window_A.get_themes()
    window_A.geometry('460x546')
    window_A.set_theme('radiance')
    window_A.title("Negative Feedback Analysis Tool")
    window_A.iconbitmap('logo.ico')
    # window_A.overrideredirect(True)
    status_bar['text'] = '>>Enter the parameters of A(s)'
    window_A_label = ttk.LabelFrame(window_A, text='A(s)')
    window_A_label.pack(fill=X)
    frame_pz_tf = ttk.Frame(window_A_label)
    frame_pz_tf.pack(fill=X, pady=10)
    sep_ = ttk.Separator(window_A_label, orient='horizontal').pack(fill=X)
    frame_pole = ttk.Frame(window_A_label)
    frame_pole.pack(fill=X, pady=20)
    sep_1 = ttk.Separator(window_A_label, orient='horizontal').pack(fill=X)
    frame_tf = ttk.Frame(window_A_label)
    frame_tf.pack(fill=X, pady=20)
    sep_2 = ttk.Separator(window_A_label, orient='horizontal').pack(fill=X)
    frame_ok = ttk.Frame(window_A_label)
    frame_ok.pack(fill=X, pady=10)
    text_2 = ttk.Label(frame_pz_tf, text='Type of input').grid(column=0, row=0, padx=20)
    string_ = tkinter.IntVar()
    tf = ttk.Radiobutton(frame_pz_tf, text='TF', value=True, variable=string_, state=NORMAL, command=input_tf)
    tf.grid(column=1, row=0, padx=70)
    pz = ttk.Radiobutton(frame_pz_tf, text='PZ', value=False, variable=string_, state=NORMAL, command=input_pz)
    pz.grid(column=2, row=0)
    text_poles = ttk.Label(frame_pole, text='Poles').grid(column=0, row=0, pady=15, padx=20)
    poles_textbox = ttk.Entry(frame_pole, textvariable=str_poles_A, state=DISABLED, width=50)
    poles_textbox.grid(column=1, row=0)
    text_zeros = ttk.Label(frame_pole, text='Zeros').grid(column=0, row=1, pady=10, padx=20)
    zeros_textbox = ttk.Entry(frame_pole, textvariable=str_zeros_A, state=DISABLED, width=50)
    zeros_textbox.grid(column=1, row=1)
    # -------------------------------------------
    text_const = ttk.Label(frame_pole, text='Constant').grid(column=0, row=2, pady=10, padx=20)
    const_textbox = ttk.Entry(frame_pole, textvariable=str_const_A, state=DISABLED, width=50)
    const_textbox.grid(column=1, row=2)
    # ---------------------------------------------
    frame_btn = ttk.Frame(frame_pole)
    frame_btn.grid(column=1, row=3, pady=10)
    enter_pz_btn = ttk.Button(frame_btn, text='Enter', state=DISABLED, width=12, command=enter_btn)
    enter_pz_btn.grid(column=0, row=0, padx=18)
    clear_pz_btn = ttk.Button(frame_btn, text='Clear', state=DISABLED, width=12, command=clear_btn)
    clear_pz_btn.grid(column=1, row=0, padx=18)

    frame_fra = ttk.Frame(frame_tf)
    frame_fra.grid(column=1, row=1, pady=20)
    text_tf = ttk.Label(frame_tf, text='TF = N(s)/D(s) = ').grid(column=0, row=1, padx=20)
    n_textbox = ttk.Entry(frame_fra, textvariable=str_num_A, state=DISABLED, width=40)
    n_textbox.grid(column=0, row=0)
    text_dash = ttk.Label(frame_fra, text='-------------------------------------------').grid(column=0, row=1)
    d_textbox = ttk.Entry(frame_fra, textvariable=str_den_A, state=DISABLED, width=40)
    d_textbox.grid(column=0, row=2)

    frame_btn_tf = ttk.Frame(frame_tf)
    frame_btn_tf.grid(column=1, row=2)
    enter_tf_btn = ttk.Button(frame_btn_tf, text='Enter', state=DISABLED, width=10, command=enter_btn_tf)
    enter_tf_btn.grid(column=0, row=0, padx=10)
    clear_tf_btn = ttk.Button(frame_btn_tf, text='Clear', state=DISABLED, width=10, command=clear_btn_tf)
    clear_tf_btn.grid(column=1, row=0)
    ok_btn = ttk.Button(frame_ok, text='OK', state=DISABLED, width=20, command=ok_fn)
    ok_btn.pack(side=BOTTOM)
    A_btn['state'] = DISABLED

    window_A.mainloop()


def get_B():
    global str_poles_B
    global str_zeros_B
    global str_den_B
    global str_num_B
    global str_const_B

    def input_pz():
        clear_btn_tf()
        poles_textbox['state'] = NORMAL
        zeros_textbox['state'] = NORMAL
        const_textbox['state'] = NORMAL
        enter_pz_btn['state'] = NORMAL
        clear_pz_btn['state'] = NORMAL
        n_textbox['state'] = DISABLED
        d_textbox['state'] = DISABLED
        enter_tf_btn['state'] = DISABLED
        clear_tf_btn['state'] = DISABLED
        poles_textbox.insert(10, 'P1 P2 P3 ....')
        zeros_textbox.insert(10, 'Z1 Z2 Z3 ....')
        global flag_tf0_pz1_B
        flag_tf0_pz1_B = 1

    def input_tf():
        clear_btn()
        poles_textbox['state'] = DISABLED
        zeros_textbox['state'] = DISABLED
        const_textbox['state'] = DISABLED
        enter_pz_btn['state'] = DISABLED
        clear_pz_btn['state'] = DISABLED
        n_textbox['state'] = NORMAL
        d_textbox['state'] = NORMAL
        enter_tf_btn['state'] = NORMAL
        clear_tf_btn['state'] = NORMAL
        n_textbox.insert(10, 'coeff of [s^n ....... s^2 s^1 s^0]')
        d_textbox.insert(10, 'coeff of [s^n ....... s^2 s^1 s^0]')
        global flag_tf0_pz1_B
        flag_tf0_pz1_B = 0

    def enter_btn():
        global str_poles_B
        str_poles_B = poles_textbox.get()
        global str_zeros_B
        str_zeros_B = zeros_textbox.get()
        global str_const_B
        str_const_B = const_textbox.get()
        ok_btn['state'] = NORMAL

    def enter_btn_tf():
        global str_num_B
        str_num_B = n_textbox.get()
        global str_den_B
        str_den_B = d_textbox.get()
        ok_btn['state'] = NORMAL

    def clear_btn():
        zeros_textbox.delete(0, 100)
        poles_textbox.delete(0, 100)
        const_textbox.delete(0, 100)

    def clear_btn_tf():
        n_textbox.delete(0, 100)
        d_textbox.delete(0, 100)

    def ok_fn():
        status_bar['text'] = '>>Welcome To NFB Analysis Tool'
        window_B.destroy()

    window_B = tk.ThemedTk()
    window_B.get_themes()
    window_B.geometry('460x546')
    window_B.set_theme('radiance')
    window_B.title("Negative Feedback Analysis Tool")
    window_B.iconbitmap('logo.ico')
    # window_B.overrideredirect(True)
    status_bar['text'] = '>>Enter the parameters of B(s)'
    window_B_label = ttk.LabelFrame(window_B, text='B(s)')
    window_B_label.pack(fill=X)
    frame_pz_tf = ttk.Frame(window_B_label)
    frame_pz_tf.pack(fill=X, pady=10)
    sep_ = ttk.Separator(window_B_label, orient='horizontal').pack(fill=X)
    frame_pole = ttk.Frame(window_B_label)
    frame_pole.pack(fill=X, pady=20)
    sep_1 = ttk.Separator(window_B_label, orient='horizontal').pack(fill=X)
    frame_tf = ttk.Frame(window_B_label)
    frame_tf.pack(fill=X, pady=20)
    sep_2 = ttk.Separator(window_B_label, orient='horizontal').pack(fill=X)
    frame_ok = ttk.Frame(window_B_label)
    frame_ok.pack(fill=X, pady=10)
    text_2 = ttk.Label(frame_pz_tf, text='Type of input').grid(column=0, row=0, padx=20)
    string_ = tkinter.IntVar()
    tf = ttk.Radiobutton(frame_pz_tf, text='TF', value=True, variable=string_, state=NORMAL, command=input_tf)
    tf.grid(column=1, row=0, padx=70)
    pz = ttk.Radiobutton(frame_pz_tf, text='PZ', value=False, variable=string_, state=NORMAL, command=input_pz)
    pz.grid(column=2, row=0)

    text_poles = ttk.Label(frame_pole, text='Poles').grid(column=0, row=0, pady=15, padx=20)
    poles_textbox = ttk.Entry(frame_pole, textvariable=str_poles_B, state=DISABLED, width=50)
    poles_textbox.grid(column=1, row=0)
    text_zeros = ttk.Label(frame_pole, text='Zeros').grid(column=0, row=1, pady=10, padx=20)
    zeros_textbox = ttk.Entry(frame_pole, textvariable=str_zeros_B, state=DISABLED, width=50)
    zeros_textbox.grid(column=1, row=1)
    # -------------------------------------------
    text_const = ttk.Label(frame_pole, text='Constant').grid(column=0, row=2, pady=10, padx=20)
    const_textbox = ttk.Entry(frame_pole, textvariable=str_const_B, state=DISABLED, width=50)
    const_textbox.grid(column=1, row=2)
    # ---------------------------------------------
    frame_btn = ttk.Frame(frame_pole)
    frame_btn.grid(column=1, row=3, pady=10)
    enter_pz_btn = ttk.Button(frame_btn, text='Enter', state=DISABLED, width=12, command=enter_btn)
    enter_pz_btn.grid(column=0, row=0, padx=18)
    clear_pz_btn = ttk.Button(frame_btn, text='Clear', state=DISABLED, width=12, command=clear_btn)
    clear_pz_btn.grid(column=1, row=0, padx=18)

    frame_fra = ttk.Frame(frame_tf)
    frame_fra.grid(column=1, row=1, pady=20)
    text_tf = ttk.Label(frame_tf, text='TF = N(s)/D(s) = ').grid(column=0, row=1, padx=20)
    n_textbox = ttk.Entry(frame_fra, textvariable=str_num_B, state=DISABLED, width=40)
    n_textbox.grid(column=0, row=0)
    text_dash = ttk.Label(frame_fra, text='-------------------------------------------').grid(column=0, row=1)
    d_textbox = ttk.Entry(frame_fra, textvariable=str_den_B, state=DISABLED, width=40)
    d_textbox.grid(column=0, row=2)

    frame_btn_tf = ttk.Frame(frame_tf)
    frame_btn_tf.grid(column=1, row=2)
    enter_tf_btn = ttk.Button(frame_btn_tf, text='Enter', state=DISABLED, width=10, command=enter_btn_tf)
    enter_tf_btn.grid(column=0, row=0, padx=10)
    clear_tf_btn = ttk.Button(frame_btn_tf, text='Clear', state=DISABLED, width=10, command=clear_btn_tf)
    clear_tf_btn.grid(column=1, row=0)
    ok_btn = ttk.Button(frame_ok, text='OK', state=DISABLED, width=20, command=ok_fn)
    ok_btn.pack(side=BOTTOM)
    B_btn['state'] = DISABLED

    window_B.mainloop()


def get_C():
    global str_poles_C
    global str_zeros_C
    global str_den_C
    global str_num_C
    global str_const_C

    def input_pz():
        clear_btn_tf()
        poles_textbox['state'] = NORMAL
        zeros_textbox['state'] = NORMAL
        const_textbox['state'] = NORMAL
        enter_pz_btn['state'] = NORMAL
        clear_pz_btn['state'] = NORMAL
        n_textbox['state'] = DISABLED
        d_textbox['state'] = DISABLED
        enter_tf_btn['state'] = DISABLED
        clear_tf_btn['state'] = DISABLED
        poles_textbox.insert(10, 'P1 P2 P3 ....')
        zeros_textbox.insert(10, 'Z1 Z2 Z3 ....')
        global flag_tf0_pz1_C
        flag_tf0_pz1_C = 1

    def input_tf():
        clear_btn()
        poles_textbox['state'] = DISABLED
        zeros_textbox['state'] = DISABLED
        const_textbox['state'] = DISABLED
        enter_pz_btn['state'] = DISABLED
        clear_pz_btn['state'] = DISABLED
        n_textbox['state'] = NORMAL
        d_textbox['state'] = NORMAL
        enter_tf_btn['state'] = NORMAL
        clear_tf_btn['state'] = NORMAL
        n_textbox.insert(10, 'coeff of [s^n ....... s^2 s^1 s^0]')
        d_textbox.insert(10, 'coeff of [s^n ....... s^2 s^1 s^0]')
        global flag_tf0_pz1_C
        flag_tf0_pz1_C = 0

    def enter_btn():
        global str_poles_C
        str_poles_C = poles_textbox.get()
        global str_zeros_C
        str_zeros_C = zeros_textbox.get()
        global str_const_C
        str_const_C = const_textbox.get()
        ok_btn['state'] = NORMAL

    def enter_btn_tf():
        global str_num_C
        str_num_C = n_textbox.get()
        global str_den_C
        str_den_C = d_textbox.get()
        ok_btn['state'] = NORMAL

    def clear_btn():
        zeros_textbox.delete(0, 100)
        poles_textbox.delete(0, 100)
        const_textbox.delete(0, 100)

    def clear_btn_tf():
        n_textbox.delete(0, 100)
        d_textbox.delete(0, 100)

    def ok_fn():
        status_bar['text'] = '>>Welcome To NFB Analysis Tool'
        window_C.destroy()

    window_C = tk.ThemedTk()
    window_C.get_themes()
    window_C.geometry('460x546')
    window_C.set_theme('radiance')
    window_C.title("Negative Feedback Analysis Tool")
    window_C.iconbitmap('logo.ico')
    # window_C.overrideredirect(True)
    status_bar['text'] = '>>Enter the parameters of C(s)'
    window_C_label = ttk.LabelFrame(window_C, text='C(s)')
    window_C_label.pack(fill=X)
    frame_pz_tf = ttk.Frame(window_C_label)
    frame_pz_tf.pack(fill=X, pady=10)
    sep_ = ttk.Separator(window_C_label, orient='horizontal').pack(fill=X)
    frame_pole = ttk.Frame(window_C_label)
    frame_pole.pack(fill=X, pady=20)
    sep_1 = ttk.Separator(window_C_label, orient='horizontal').pack(fill=X)
    frame_tf = ttk.Frame(window_C_label)
    frame_tf.pack(fill=X, pady=20)
    sep_2 = ttk.Separator(window_C_label, orient='horizontal').pack(fill=X)
    frame_ok = ttk.Frame(window_C_label)
    frame_ok.pack(fill=X, pady=10)
    text_2 = ttk.Label(frame_pz_tf, text='Type of input').grid(column=0, row=0, padx=20)
    storing = tkinter.IntVar()
    tf = ttk.Radiobutton(frame_pz_tf, text='TF', value=True, variable=storing, state=NORMAL, command=input_tf)
    tf.grid(column=1, row=0, padx=70)
    pz = ttk.Radiobutton(frame_pz_tf, text='PZ', value=False, variable=storing, state=NORMAL, command=input_pz)
    pz.grid(column=2, row=0)

    text_poles = ttk.Label(frame_pole, text='Poles').grid(column=0, row=0, pady=15, padx=20)
    poles_textbox = ttk.Entry(frame_pole, textvariable=str_poles_C, state=DISABLED, width=50)
    poles_textbox.grid(column=1, row=0)
    text_zeros = ttk.Label(frame_pole, text='Zeros').grid(column=0, row=1, pady=10, padx=20)
    zeros_textbox = ttk.Entry(frame_pole, textvariable=str_zeros_C, state=DISABLED, width=50)
    zeros_textbox.grid(column=1, row=1)
    # -------------------------------------------
    text_const = ttk.Label(frame_pole, text='Constant').grid(column=0, row=2, pady=10, padx=20)
    const_textbox = ttk.Entry(frame_pole, textvariable=str_const_C, state=DISABLED, width=50)
    const_textbox.grid(column=1, row=2)
    # ---------------------------------------------
    frame_btn = ttk.Frame(frame_pole)
    frame_btn.grid(column=1, row=3, pady=10)
    enter_pz_btn = ttk.Button(frame_btn, text='Enter', state=DISABLED, width=12, command=enter_btn)
    enter_pz_btn.grid(column=0, row=0, padx=18)
    clear_pz_btn = ttk.Button(frame_btn, text='Clear', state=DISABLED, width=12, command=clear_btn)
    clear_pz_btn.grid(column=1, row=0, padx=18)
    frame_fra = ttk.Frame(frame_tf)
    frame_fra.grid(column=1, row=1, pady=20)
    text_tf = ttk.Label(frame_tf, text='TF = N(s)/D(s) = ').grid(column=0, row=1, padx=20)
    n_textbox = ttk.Entry(frame_fra, textvariable=str_num_C, state=DISABLED, width=40)
    n_textbox.grid(column=0, row=0)
    text_dash = ttk.Label(frame_fra, text='-------------------------------------------').grid(column=0, row=1)
    d_textbox = ttk.Entry(frame_fra, textvariable=str_den_C, state=DISABLED, width=40)
    d_textbox.grid(column=0, row=2)

    frame_btn_tf = ttk.Frame(frame_tf)
    frame_btn_tf.grid(column=1, row=2)
    enter_tf_btn = ttk.Button(frame_btn_tf, text='Enter', state=DISABLED, width=10, command=enter_btn_tf)
    enter_tf_btn.grid(column=0, row=0, padx=10)
    clear_tf_btn = ttk.Button(frame_btn_tf, text='Clear', state=DISABLED, width=10, command=clear_btn_tf)
    clear_tf_btn.grid(column=1, row=0)
    ok_btn = ttk.Button(frame_ok, text='OK', state=DISABLED, width=20, command=ok_fn)
    ok_btn.pack(side=BOTTOM)
    C_btn['state'] = DISABLED

    window_C.mainloop()


def clear_table():
    selected_item = table.selection()[0]
    table.delete(selected_item)


# ----------setup window-------
window1 = tk.ThemedTk()
window1.get_themes()
window1.set_theme('radiance')
window1.state('zoomed')
window1.title("Negative Feedback Analysis Tool (Beta Version)")
window1.iconbitmap('logo.ico')
status_bar = ttk.Label(window1, text='>>Welcome to NFB Analysis Tool', relief=GROOVE, anchor=W, font='Arial 11 bold')
status_bar.pack(side=BOTTOM, fill=X)
# ------global variables-----------
str_poles_A = tkinter.StringVar()
str_zeros_A = tkinter.StringVar()
str_const_A = tkinter.StringVar()
str_num_A = tkinter.StringVar()
str_den_A = tkinter.StringVar()
str_poles_B = tkinter.StringVar()
str_zeros_B = tkinter.StringVar()
str_const_B = tkinter.StringVar()
str_num_B = tkinter.StringVar()
str_den_B = tkinter.StringVar()
str_poles_C = tkinter.StringVar()
str_zeros_C = tkinter.StringVar()
str_const_C = tkinter.StringVar()
str_num_C = tkinter.StringVar()
str_den_C = tkinter.StringVar()
flag_tf0_pz1_A = -1
flag_tf0_pz1_B = -1
flag_tf0_pz1_C = -1
inputs = []
data = []
# ----------menu bar----------
menu_bar = Menu(window1)
window1.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
edit_menu = Menu(menu_bar, tearoff=0)
view_menu = Menu(menu_bar, tearoff=0)
run_menu = Menu(menu_bar, tearoff=0)
tools_menu = Menu(menu_bar, tearoff=0)
tabs_menu = Menu(menu_bar, tearoff=0)
help_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New...')
file_menu.add_command(label='Open...')
file_menu.add_command(label='Save')
file_menu.add_command(label='Load')
file_menu.add_command(label='Exit')
help_menu.add_command(label='Help Browser')
help_menu.add_command(label='About')
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="View", menu=view_menu)
menu_bar.add_cascade(label="Run", menu=run_menu)
menu_bar.add_cascade(label="Tools", menu=tools_menu)
menu_bar.add_cascade(label="Tabs", menu=tabs_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)
# ------define frames-------
left_label_frame = ttk.LabelFrame(window1, text='Menu')
left_label_frame.pack(side=LEFT, fill='y')
run = PhotoImage(file='run_btn.png')
stop = PhotoImage(file='stop_btn.png')
reset = PhotoImage(file='reset_btn.png')
check = PhotoImage(file='check.png')
open_ = PhotoImage(file='open.png')
save = PhotoImage(file='save.png')
help_ = PhotoImage(file='help.png')
exit_ = PhotoImage(file='exit.png')
check_btn = ttk.Button(left_label_frame, image=check, command=check_fn)
check_btn.grid(column=0, row=0)
check_text = ttk.Label(left_label_frame, text='Check').grid(column=0, row=1)
run_btn = ttk.Button(left_label_frame, image=run, state=DISABLED, command=run_fn)
run_btn.grid(column=0, row=2)
run_text = ttk.Label(left_label_frame, text='Run').grid(column=0, row=3)
stop_btn = ttk.Button(left_label_frame, image=stop).grid(column=0, row=4)
stop_text = ttk.Label(left_label_frame, text='Stop').grid(column=0, row=5)
reset_btn = ttk.Button(left_label_frame, image=reset, command=reset_fn)
reset_btn.grid(column=0, row=6)
reset_text = ttk.Label(left_label_frame, text='Reset').grid(column=0, row=7)
sep = ttk.Label(left_label_frame, text='• • •').grid(column=0, row=8, pady=5)
open_btn = ttk.Button(left_label_frame, image=open_).grid(column=0, row=9)
open_text = ttk.Label(left_label_frame, text='Open').grid(column=0, row=10)
save_btn = ttk.Button(left_label_frame, image=save).grid(column=0, row=11)
save_text = ttk.Label(left_label_frame, text='Save').grid(column=0, row=12)
help_btn = ttk.Button(left_label_frame, image=help_).grid(column=0, row=13)
help_text = ttk.Label(left_label_frame, text='Help').grid(column=0, row=14)
exit_btn = ttk.Button(left_label_frame, image=exit_, command=exit_fn).grid(column=0, row=15)
exit_text = ttk.Label(left_label_frame, text='Exit').grid(column=0, row=16)
# -------------------end of left frame------------------------------------
mid_label_frame = ttk.Frame(window1)
mid_label_frame.place(x=70, y=0)
NFB_block_label_frame = ttk.LabelFrame(mid_label_frame, text='Block Diagram')
NFB_block_label_frame.pack()
NFB_block = PhotoImage(file='NFB_block.png')
NFB_block_photo = Label(NFB_block_label_frame, image=NFB_block).grid(column=0, row=0)
inputs_frame = ttk.LabelFrame(mid_label_frame, text='Input Panel')
inputs_frame.pack(fill=Y)
text1_frame = ttk.Frame(inputs_frame)
text1_frame.pack()
text_1 = ttk.Label(text1_frame, text='Enter the parameters of all blocks, then press on check to validate inputs').grid(
    column=0, row=0, pady=10)
abs_frame = ttk.Frame(inputs_frame)
abs_frame.pack()
A_btn = ttk.Button(abs_frame, text='A(s)', width=16, command=get_A)
A_btn.grid(column=0, row=1, padx=17, pady=15)
B_btn = ttk.Button(abs_frame, text='B(s)', width=16, command=get_B)
B_btn.grid(column=1, row=1, padx=17, pady=15)
C_btn = ttk.Button(abs_frame, text='C(s)', width=16, command=get_C)
C_btn.grid(column=2, row=1, padx=17, pady=15)
status_bar['text'] = '>>Welcome To NFB Analysis Tool'
sep_3 = ttk.Separator(inputs_frame, orient='horizontal').pack(fill=X)
# --------------------------------------------------------------------------


inputs_view_frame = ttk.Frame(inputs_frame, height=1000)
inputs_view_frame.pack(fill=Y)
s = ttk.Style()
s.configure('Treeview', rowheight=32)
table = ttk.Treeview(inputs_view_frame)
table['columns'] = ('Poles', 'Zeros', 'Numerator Polynomial', 'Denominator Polynomial')
table.column('#0', width=60, minwidth=50)
table.column('Poles', width=110, minwidth=50, anchor=tkinter.CENTER)
table.column('Zeros', width=110, minwidth=50, anchor=tkinter.CENTER)
table.column('Numerator Polynomial', width=158, minwidth=50, anchor=tkinter.CENTER)
table.column('Denominator Polynomial', width=158, minwidth=50, anchor=tkinter.CENTER)
# ---------------------------------------------------------------------------------
table.heading('#0', text='Block')
table.heading('Poles', text='Poles', anchor=tkinter.CENTER)
table.heading('Zeros', text='Zeros', anchor=tkinter.CENTER)
table.heading('Numerator Polynomial', text='Numerator Poly', anchor=tkinter.CENTER)
table.heading('Denominator Polynomial', text='Denominator Poly', anchor=tkinter.CENTER)
# -------------------------------------------------------------------------------------------
table.insert('', 0, text='A(s)', values=('-', '-', '-', '-'))
table.insert('', 1, text='B(s)', values=('-', '-', '-', '-'))
table.insert('', 2, text='C(s)', values=('-', '-', '-', '-'))
table.insert('', 3, text='LG(s)', values=('-', '-', '-', '-'))
table.insert('', 4, text='CL(s)', values=('-', '-', '-', '-'))
table.pack()
clear_btn_table = ttk.Button(inputs_view_frame, text='Clear', command=clear_table)
clear_btn_table.pack(side=TOP)
#-------------------right frame--------------------------------------------------------
right_label_frame = ttk.LabelFrame(window1, text='Output Panel')
right_label_frame.place(x=680,y=0)
l = ttk.Label(right_label_frame, text='Frequency response')
l.pack()
window1.mainloop()
