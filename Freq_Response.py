from typing import Any, Union

import numpy as np
from control import TransferFunction
from matplotlib import pyplot as plt
import control.matlab as mt
import cmath


def str2num(str_arr, flag_pz):
    arr_num = []
    num = 0
    if len(str_arr) == 1 and flag_pz == 1:
        if len(str_arr[0]) == 0:
            return arr_num

    for i in range(0, len(str_arr)):
        suffix = str_arr[i][len(str_arr[i]) - 1]
        if suffix == 'G':
            str_arr[i] = str_arr[i].removesuffix('G')
            num = float(str_arr[i]) * pow(10, 9)
        elif suffix == 'M':
            str_arr[i] = str_arr[i].removesuffix('M')
            num = float(str_arr[i]) * pow(10, 6)
        elif suffix == 'K':
            str_arr[i] = str_arr[i].removesuffix('K')
            num = float(str_arr[i]) * pow(10, 3)
        elif suffix == 'k':
            str_arr[i] = str_arr[i].removesuffix('k')
            num = float(str_arr[i]) * pow(10, 3)
        elif suffix == 'j':  # processing complex PZ
            str_arr[i] = str_arr[i].removesuffix('j')
            temp_real = ''
            temp_img = ''
            flag = 0
            for j in range(0, len(str_arr[i])):
                if (str_arr[i][j] not in '+-') and flag == 0:
                    temp_real = temp_real + str_arr[i][j]
                elif (str_arr[i][j] == '+') and flag == 0:
                    flag = 1
                elif (str_arr[i][j] == '-') and flag == 0:
                    flag = 1
                    temp_img = temp_img + str_arr[i][j]
                elif (str_arr[i][j] not in '+-') and flag == 1:
                    temp_img = temp_img + str_arr[i][j]
            # -------------------real_part------------------------------
            num_real = 0
            suffix_real = temp_real[len(temp_real) - 1]
            if suffix_real == 'G':
                temp_real = temp_real.removesuffix('G')
                num_real = float(temp_real) * pow(10, 9)
            elif suffix_real == 'M':
                temp_real = temp_real.removesuffix('M')
                num_real = float(temp_real) * pow(10, 6)
            elif suffix_real == 'K':
                temp_real = temp_real.removesuffix('K')
                num_real = float(temp_real) * pow(10, 3)
            elif suffix_real == 'k':
                temp_real = temp_real.removesuffix('k')
                num_real = float(temp_real) * pow(10, 3)
            else:
                num_real = float(temp_real)
            num = complex(num_real, float(temp_img))
        else:
            num = float(str_arr[i])
        arr_num.insert(i, num)
    return arr_num


def str1_2_num(str_):
    suffix = str_[len(str_) - 1]
    if suffix == 'G':
        str_ = str_.removesuffix('G')
        num = float(str_) * pow(10, 9)
    elif suffix == 'M':
        str_ = str.removesuffix('M')
        num = float(str_) * pow(10, 6)
    elif suffix == 'K':
        str_ = str_.removesuffix('K')
        num = float(str_) * pow(10, 3)
    elif suffix == 'k':
        str_ = str_.removesuffix('k')
        num = float(str_) * pow(10, 3)
    else:
        num = float(str_)

    return num


def str2arr(string_):
    str1 = string_ + ' '
    arr1 = []
    index = 0
    temp = ''
    for i in range(0, len(str1)):
        if str1[i] != ' ':
            temp = temp + str1[i]
        elif str1[i] == ' ':
            arr1.insert(index, temp)
            temp = ''
            index = index + 1
    return arr1


def dB2mag(value):
    return 10 ^ (value / 20)


def generate_freq(start_freq_rad, end_freq_rad, step):
    no_of_pts = int(np.ceil((end_freq_rad - start_freq_rad) / step))
    f = 0
    freq = []
    for i in range(0, no_of_pts):
        f = start_freq_rad + i * step
        freq.insert(i, f)

    return freq


def append2first(list1, value):
    temp = [value]
    for i in range(0, len(list1)):
        temp.append(list1[i])
    return temp


def add_elm_by_elm(list1, list2):
    l = []
    for i in range(0, len(list1)):
        l.insert(i, list1[i] + list2[i])
    return l


def conv_list2arr(list1):
    return np.array(list1)


def conv_arr2list(arr):
    l = []
    for i in range(0, len(arr)):
        l.insert(i, arr[i])
    return l


def push(value, list1):
    return list1 + [value]


def get_TF(zeros, poles, constant):
    num_fact = []
    den_fact = []
    i = 0

    while i < len(zeros):
        num_fact.insert(i, [1, -1 * zeros[i]])
        i = i + 1
    i = 0
    while i < len(poles):
        den_fact.insert(i, [1, -1 * poles[i]])
        i = i + 1
    i = 0
    num = [1]
    den = [1]
    while i < (len(zeros)):
        num = np.polymul(num, num_fact[i])
        i = i + 1
    i = 0
    while i < len(poles):
        den = np.polymul(den, den_fact[i])
        i = i + 1

    H_s = constant * mt.tf(num, den)
    # print(H_s)
    d, n = [], []
    for i in range(0, len(num)):
        n.append(num[i].real * constant)

    for i in range(0, len(den)):
        d.append(den[i].real)

    return H_s, n, d


def num_den_TF(num_list, den_list, constant):
    num_arr = conv_list2arr(num_list)
    den_arr = conv_list2arr(den_list)
    H_s = constant * mt.tf(num_arr, den_arr)
    return H_s


def get_PZ(TF):
    poles = mt.pole(TF)
    zeros = mt.zero(TF)
    return zeros, poles


def BodePlot(TF, freq_range, show_plot):
    mag, phase, w = mt.bode(TF, freq_range)
    if show_plot != 0:
        plt.show()
    return mag, phase, w


def DC_gain_dB(TF, freq_range):
    mag, phase, w = BodePlot(TF, freq_range, 0)
    dc_gain = np.max(mag)
    dc_gain_dB = 20 * np.log10(dc_gain)
    return dc_gain_dB


def find_min(list1):
    min_list1 = list1[0]
    min_index = 0
    for i in range(1, len(list1)):
        if list1[i] < min_list1:
            min_list1 = list1[i]
            min_index = i
    return min_index, min_list1


def mag2dB_list(list1):
    out = []
    for i in range(0, len(list1)):
        out.insert(i, 20 * np.log10(list1[i]))
    return out


def BandWidth_LPF(TF, freq_range):
    mag, phase, w = BodePlot(TF, freq_range, 0)
    dB_3 = DC_gain_dB(TF, freq_range) - 3
    mag = mag2dB_list(mag)
    i = 0
    diff = []
    while i < len(mag):
        diff.insert(i, np.abs(mag[i] - dB_3))
        i = i + 1
    index, val = find_min(diff)
    BW = w[index]
    return BW


def BandWidth_BPF(TF, freq_range):
    mag, phase, w = BodePlot(TF, freq_range, 0)
    dB_3 = DC_gain_dB(TF, freq_range) - 3
    mag = mag2dB_list(mag)
    index = []
    flag = 0
    for i in range(0, len(mag)):
        if (np.abs(mag[i] - dB_3) < 0.02) & (flag == 0):
            index = push(i, index)
            flag = 1
        if (np.abs(mag[i] - dB_3) > 2) & (flag == 1):
            flag = 0
    BW = w[index[1]] - w[index[0]]
    return BW


def ClosedLoop_TF(AOL_TF, Beta_TF, C_s):
    n1 = AOL_TF.num[0][0]
    d1 = AOL_TF.den[0][0]
    n2 = Beta_TF.num[0][0]
    d2 = Beta_TF.den[0][0]
    n1 = conv_arr2list(n1)
    d1 = conv_arr2list(d1)
    n2 = conv_arr2list(n2)
    d2 = conv_arr2list(d2)

    num = np.polymul(conv_list2arr(n1), conv_list2arr(d2))
    den1 = np.polymul(conv_list2arr(d1), conv_list2arr(d2))
    den2 = np.polymul(conv_list2arr(n1), conv_list2arr(n2))
    den1 = conv_arr2list(den1)
    den2 = conv_arr2list(den2)
    if len(den1) > len(den2):
        i = len(den2)
        while i < len(den1):
            den2 = append2first(den2, 0)
            i = i + 1
    else:
        i = len(den1)
        while i < len(den2):
            den1 = append2first(den1, 0)
            i = i + 1

    den = conv_list2arr(add_elm_by_elm(den2, den1))
    CL_TF = C_s * mt.tf(num, den)
    num_cl = CL_TF.num
    den_cl = CL_TF.den
    return CL_TF, num_cl[0][0], den_cl[0][0]


def get_CornerFreq(TF, freq_range):
    mag, phase, w = BodePlot(TF, freq_range, 0)
    dB_3 = DC_gain_dB(TF, freq_range) - 3
    mag = mag2dB_list(mag)
    index = []
    corn_freq = []
    flag = 0
    for i in range(0, len(mag)):
        if (np.abs(mag[i] - dB_3) < 0.02) & (flag == 0):
            index = push(i, index)
            corn_freq.append(w[i])
            flag = 1
        if (np.abs(mag[i] - dB_3) > 2) & (flag == 1):
            flag = 0

    return corn_freq


def BPF_QualityFactor(TF, freq_range):
    BW = BandWidth_BPF(TF, freq_range)
    corner_freq = get_CornerFreq(TF, freq_range)
    center_freq = 0.5 * (corner_freq[0] + corner_freq[1])
    Q = center_freq / BW
    return Q


def LoopGain(Aol_s, Beta_s):
    print(Aol_s)
    print(Beta_s)
    LG = Aol_s * Beta_s
    print(LG)
    num_lg = LG.num
    den_lg = LG.den
    return LG, num_lg[0][0], den_lg[0][0]


def get_data(TF, freq_range, input_str_w_mag_ph, input_value):
    mag, phase, w = BodePlot(TF, freq_range, 0)
    mag = conv_arr2list(mag)
    phase = conv_arr2list(phase)
    w = conv_arr2list(w)
    mag = mag2dB_list(mag)
    if input_str_w_mag_ph == 'w':
        min_diff = 10000000
        min_diff_index = 0
        for i in range(0, len(w)):
            diff = np.abs(input_value - w[i])
            if diff < min_diff:
                min_diff = diff
                min_diff_index = i
        return mag[min_diff_index], (180 / np.pi) * phase[min_diff_index]
    elif input_str_w_mag_ph == 'mag':
        min_diff = 10000000
        min_diff_index = 0
        for i in range(0, len(mag)):
            diff = np.abs(input_value - mag[i])
            if diff < min_diff:
                min_diff = diff
                min_diff_index = i
        return w[min_diff_index], (180 / np.pi) * phase[min_diff_index]
    elif input_str_w_mag_ph == 'ph':
        input_value = (np.pi / 180) * input_value
        min_diff = 10000000
        min_diff_index = 0
        for i in range(0, len(phase)):
            diff = np.abs(input_value - phase[i])
            if diff < min_diff:
                min_diff = diff
                min_diff_index = i
        return w[min_diff_index], mag[min_diff_index]
    else:
        return False


def phase_margin_deg(TF, freq_range):
    w_0dB, phase_0dB = get_data(TF, freq_range, 'mag', 0)
    PM = 180 + phase_0dB
    if 0 < PM < 90:
        return PM
    elif PM < 0:
        return False
    elif PM > 90:
        return True


def gain_margin_dB(TF, freq_range):
    w_0dB, mag_0dB = get_data(TF, freq_range, 'ph', -180)
    GM = 0 - mag_0dB
    if GM > 0:
        return GM
    else:
        return False


def UnityGainFreq_rad(TF, freq_range):
    w_0dB, phase_0dB = get_data(TF, freq_range, 'mag', 0)
    return w_0dB


def GBW_rad(TF, freq_range):
    GBW = dB2mag(DC_gain_dB(TF, freq_range)) * BandWidth_LPF(TF, freq_range)
    return GBW


def create_data(num_A, den_A, num_B, den_B, num_C, den_C, p_A, z_A, p_B, z_B, p_C, z_C, flag_tf0_pz1_A, flag_tf0_pz1_B,
                flag_tf0_pz1_C, const_A, const_B, const_C):
    poles_A, zeros_A, n_A, d_A = '', '', '', ''
    poles_B, zeros_B, n_B, d_B = '', '', '', ''
    poles_C, zeros_C, n_C, d_C = '', '', '', ''
    # ------------------------------A-------------------------------------------
    if flag_tf0_pz1_A == 0:
        for i in range(0, len(num_A)):
            temp = num2str_suffix(num_A[i])
            if temp[0] != '-':
                n_A = n_A + '+' + temp + 'S^' + str(len(num_A) - i - 1)
            elif temp[0] == '-':
                n_A = n_A + temp + 'S^' + str(len(num_A) - i - 1)
        for i in range(0, len(den_A)):
            temp = num2str_suffix(den_A[i])
            if temp[0] != '-':
                d_A = d_A + '+' + temp + 'S^' + str(len(den_A) - i - 1)
            elif temp[0] == '-':
                d_A = d_A + temp + 'S^' + str(len(den_A) - i - 1)
        n_A = n_A[0:len(n_A) - 3]
        d_A = d_A[0:len(d_A) - 3]
        if n_A[0] == '+':
            n_A = n_A[1:len(n_A)]
        if d_A[0] == '+':
            d_A = d_A[1:len(d_A)]
        # global TF_A
        TFA = num_den_TF(num_A, den_A, 1)
        ze_A, po_A = get_PZ(TFA)
        for i in range(0, len(po_A)):
            temp = num2str_suffix(po_A[i])
            poles_A = poles_A + temp + ' ,'
        for i in range(0, len(ze_A)):
            temp = num2str_suffix(ze_A[i])
            zeros_A = zeros_A + temp + ' ,'
        poles_A = poles_A[0:len(poles_A) - 1]
        zeros_A = zeros_A[0:len(zeros_A) - 1]
    elif flag_tf0_pz1_A == 1:
        for i in range(0, len(p_A)):
            temp = num2str_suffix(p_A[i])
            poles_A = poles_A + temp + ' ,'
        for i in range(0, len(z_A)):
            temp = num2str_suffix(z_A[i])
            zeros_A = zeros_A + temp + ' ,'
        poles_A = poles_A[0:len(poles_A) - 1]
        zeros_A = zeros_A[0:len(zeros_A) - 1]
        TFA, num, den = get_TF(z_A, p_A, const_A)
        for i in range(0, len(num)):
            temp = num2str_suffix(num[i])
            if temp[0] != '-':
                n_A = n_A + '+' + temp + 'S^' + str(len(num) - i - 1)
            elif temp[0] == '-':
                n_A = n_A + temp + 'S^' + str(len(num) - i - 1)
        for i in range(0, len(den)):
            temp = num2str_suffix(den[i])
            if temp[0] != '-':
                d_A = d_A + '+' + temp + 'S^' + str(len(den) - i - 1)
            elif temp[0] == '-':
                d_A = d_A + temp + 'S^' + str(len(den) - i - 1)
        n_A = n_A[0:len(n_A) - 3]
        d_A = d_A[0:len(d_A) - 3]
        if n_A[0] == '+':
            n_A = n_A[1:len(n_A)]
        if d_A[0] == '+':
            d_A = d_A[1:len(d_A)]
    # --------------------------------------------------------------------------------
    # ------------------------------B-------------------------------------------
    if flag_tf0_pz1_B == 0:
        for i in range(0, len(num_B)):
            temp = num2str_suffix(num_B[i])
            if temp[0] != '-':
                n_B = n_B + '+' + temp + 'S^' + str(len(num_B) - i - 1)
            elif temp[0] == '-':
                n_B = n_B + temp + 'S^' + str(len(num_B) - i - 1)
        for i in range(0, len(den_B)):
            temp = num2str_suffix(den_B[i])
            if temp[0] != '-':
                d_B = d_B + '+' + temp + 'S^' + str(len(den_B) - i - 1)
            elif temp[0] == '-':
                d_B = d_B + temp + 'S^' + str(len(den_B) - i - 1)
        n_B = n_B[0:len(n_B) - 3]
        d_B = d_B[0:len(d_B) - 3]
        if n_B[0] == '+':
            n_B = n_B[1:len(n_B)]
        if d_B[0] == '+':
            d_B = d_B[1:len(d_B)]
        TFB = num_den_TF(num_B, den_B, 1)
        ze_B, po_B = get_PZ(TFB)
        for i in range(0, len(po_B)):
            temp = num2str_suffix(po_B[i])
            poles_B = poles_B + temp + ' ,'
        for i in range(0, len(ze_B)):
            temp = num2str_suffix(ze_B[i])
            zeros_B = zeros_B + temp + ' ,'
        poles_B = poles_B[0:len(poles_B) - 1]
        zeros_B = zeros_B[0:len(zeros_B) - 1]
    elif flag_tf0_pz1_B == 1:
        for i in range(0, len(p_B)):
            temp = num2str_suffix(p_B[i])
            poles_B = poles_B + temp + ' ,'
        for i in range(0, len(z_B)):
            temp = num2str_suffix(z_B[i])
            zeros_B = zeros_B + temp + ' ,'
        poles_B = poles_B[0:len(poles_B) - 1]
        zeros_B = zeros_B[0:len(zeros_B) - 1]
        TFB, num, den = get_TF(z_B, p_B, const_B)
        for i in range(0, len(num)):
            temp = num2str_suffix(num[i])
            if temp[0] != '-':
                n_B = n_B + '+' + temp + 'S^' + str(len(num) - i - 1)
            elif temp[0] == '-':
                n_B = n_B + temp + 'S^' + str(len(num) - i - 1)
        for i in range(0, len(den)):
            temp = num2str_suffix(den[i])
            if temp[0] != '-':
                d_B = d_B + '+' + temp + 'S^' + str(len(den) - i - 1)
            elif temp[0] == '-':
                d_B = d_B + temp + 'S^' + str(len(den) - i - 1)
        n_B = n_B[0:len(n_B) - 3]
        d_B = d_B[0:len(d_B) - 3]
        if n_B[0] == '+':
            n_B = n_B[1:len(n_B)]
        if d_B[0] == '+':
            d_B = d_B[1:len(d_B)]
    # -----------------------------------C---------------------------------------------
    if flag_tf0_pz1_C == 0:
        for i in range(0, len(num_C)):
            temp = num2str_suffix(num_C[i])
            if temp[0] != '-':
                n_C = n_C + '+' + temp + 'S^' + str(len(num_C) - i - 1)
            elif temp[0] == '-':
                n_C = n_C + temp + 'S^' + str(len(num_C) - i - 1)
        for i in range(0, len(den_C)):
            temp = num2str_suffix(den_C[i])
            if temp[0] != '-':
                d_C = d_C + '+' + temp + 'S^' + str(len(den_C) - i - 1)
            elif temp[0] == '-':
                d_C = d_C + temp + 'S^' + str(len(den_C) - i - 1)
        n_C = n_C[0:len(n_C) - 3]
        d_C = d_C[0:len(d_C) - 3]
        if n_C[0] == '+':
            n_C = n_C[1:len(n_C)]
        if d_C[0] == '+':
            d_C = d_C[1:len(d_C)]
        TFC = num_den_TF(num_C, den_C, 1)
        ze_C, po_C = get_PZ(TFC)
        for i in range(0, len(po_C)):
            temp = num2str_suffix(po_C[i])
            poles_C = poles_C + temp + ' ,'
        for i in range(0, len(ze_C)):
            temp = num2str_suffix(ze_C[i])
            zeros_C = zeros_C + temp + ' ,'
        poles_C = poles_C[0:len(poles_C) - 1]
        zeros_C = zeros_C[0:len(zeros_C) - 1]
    elif flag_tf0_pz1_C == 1:
        for i in range(0, len(p_C)):
            temp = num2str_suffix(p_C[i])
            poles_C = poles_C + temp + ' ,'
        for i in range(0, len(z_C)):
            temp = num2str_suffix(z_C[i])
            zeros_C = zeros_C + temp + ' ,'
        poles_C = poles_C[0:len(poles_C) - 1]
        zeros_C = zeros_C[0:len(zeros_C) - 1]
        TFC, num, den = get_TF(z_C, p_C, const_C)
        for i in range(0, len(num)):
            temp = num2str_suffix(num[i])
            if temp[0] != '-':
                n_C = n_C + '+' + temp + 'S^' + str(len(num) - i - 1)
            elif temp[0] == '-':
                n_C = n_C + temp + 'S^' + str(len(num) - i - 1)
        for i in range(0, len(den)):
            temp = num2str_suffix(den[i])
            if temp[0] != '-':
                d_C = d_C + '+' + temp + 'S^' + str(len(den) - i - 1)
            elif temp[0] == '-':
                d_C = d_C + temp + 'S^' + str(len(den) - i - 1)
        n_C = n_C[0:len(n_C) - 3]
        d_C = d_C[0:len(d_C) - 3]
        if n_C[0] == '+':
            n_C = n_C[1:len(n_C)]
        if d_C[0] == '+':
            d_C = d_C[1:len(d_C)]
        # --------------------------------------------------------------------------------

    data = [(poles_A, zeros_A, n_A, d_A), (poles_B, zeros_B, n_B, d_B), (poles_C, zeros_C, n_C, d_C)]
    return data


def num2str_suffix(num):
    suffix_mapper = {1: 'K',
                     2: 'M',
                     3: 'G'
                     }
    out = ''
    sign = 0
    num_x = num
    if complex(num_x).imag == 0:
        if num_x < 0:
            sign = 1
            num_x = np.abs(num_x)
        flag = 0
        for i in range(1, 4):
            temp = np.floor(num_x / (1000 ** i))
            if temp != 0:
                temp = num_x / (1000 ** i)
                if sign == 1:
                    out = '-' + str(temp) + suffix_mapper[i]
                else:
                    out = str(temp) + suffix_mapper[i]
                flag = 1
            elif temp == 0 and flag == 0:
                if sign == 1:
                    return '-' + str(num_x)
                else:
                    return str(num_x)
        return out
    elif complex(num_x).imag != 0:
        real_part = complex(num_x).real
        img_part = complex(num_x).imag
        sign_real = 0
        sign_img = 0
        if real_part < 0:
            sign_real = 1
            real_part = np.abs(real_part)
        if img_part < 0:
            sign_img = 1
            img_part = np.abs(img_part)
        flag = 0
        for i in range(1, 4):
            temp_real = np.floor(real_part / (1000 ** i))
            if temp_real != 0:
                temp_real = real_part / (1000 ** i)
                if sign_real == 1:
                    if sign_img == 1:
                        out = '[-' + str(temp_real) + suffix_mapper[i] + '-' + str(img_part) + 'j]'
                    elif sign_img == 0:
                        out = '[-' + str(temp_real) + suffix_mapper[i] + '+' + str(img_part) + 'j]'
                else:
                    if sign_img == 1:
                        out = '[' + str(temp_real) + suffix_mapper[i] + '-' + str(img_part) + 'j]'
                    elif sign_img == 0:
                        out = '[' + str(temp_real) + suffix_mapper[i] + '+' + str(img_part) + 'j]'
                flag = 1
            elif temp_real == 0 and flag == 0:
                if sign_real == 1:
                    if sign_img == 1:
                        return '[-' + str(real_part) + '-' + str(img_part) + 'j]'
                    elif sign_img == 0:
                        return '[-' + str(real_part) + '+' + str(img_part) + 'j]'
                else:
                    if sign_img == 1:
                        return '[' + str(real_part) + '-' + str(img_part) + 'j]'
                    elif sign_img == 0:
                        return '[' + str(real_part) + '+' + str(img_part) + 'j]'

        return out


# CL_s, num_cl, den_cl = ClosedLoop_TF(TF_A, TF_B, TF_C)
# LG_s, num_lg, den_lg = LoopGain(TF_A, TF_B)


def generate_num_den_pz(TF, num, den):
    poles, zeros, n, d = '', '', '', ''
    for i in range(0, len(num)):
        temp = num2str_suffix(num[i])
        if temp[0] != '-':
            n = n + '+' + temp + 'S^' + str(len(num) - i - 1)
        elif temp[0] == '-':
            n = n + temp + 'S^' + str(len(num) - i - 1)
    for i in range(0, len(den)):
        temp = num2str_suffix(den[i])
        if temp[0] != '-':
            d = d + '+' + temp + 'S^' + str(len(den) - i - 1)
        elif temp[0] == '-':
            d = d + temp + 'S^' + str(len(den) - i - 1)
    n = n[0:len(n) - 3]
    d = d[0:len(d) - 3]
    if n[0] == '+':
        n = n[1:len(n)]
    if d[0] == '+':
        d = d[1:len(d)]
    ze, po = get_PZ(TF)
    for i in range(0, len(po)):
        temp = num2str_suffix(po[i])
        poles = poles + temp + ' ,'
    for i in range(0, len(ze)):
        temp = num2str_suffix(ze[i])
        zeros = zeros + temp + ' ,'
    poles = poles[0:len(poles) - 1]
    zeros = zeros[0:len(zeros) - 1]
    return poles, zeros, n, d
