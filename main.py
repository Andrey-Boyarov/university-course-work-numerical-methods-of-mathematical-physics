from tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def place_input(label, x, y, default):
    lbl = Label(window, text=label)
    lbl.place(x=x, y=y)
    txt = Entry(window, width=15)
    txt.place(x=x + 120, y=y)
    txt.insert(0, default)
    return txt


def calculate_data():
    k_k = float(inp_k_k.get())
    c = float(inp_c.get())
    alpha = float(inp_alpha.get())
    u_0 = float(inp_u0.get())
    l = float(inp_l.get())
    S = float(inp_S.get())
    T = float(inp_T.get())
    I = int(inp_I.get())
    K = int(inp_K.get())
    cut = int(inp_cut.get())

    ht = T / K
    hx = l / I
    R = np.sqrt(S / np.pi)

    u = np.zeros((K + 1, I + 1))

    t = np.linspace(0, T, K + 1)
    z = np.linspace(0, l, I + 1)

    phi = np.sin(np.pi * z / l) ** 2

    def difference_scheme():

        for k in range(0, K):
            u[0, 1:I] = u_0
            u[k + 1, 0] = u[k, 0] * (
                        1 - 2 * k_k * ht / c / hx / hx - 2 * alpha * ht / c / R) + 2 * k_k * ht / c / hx / hx * u[
                              k, 1] + ht / c * phi[0]
            u[k + 1, 1:I] = u[k, 1:I] * (
                        1 - 2 * k_k * ht / c / hx / hx - 2 * alpha * ht / c / R) + k_k * ht / c / hx / hx * (
                                        u[k, 0:I - 1] + u[k, 2:I + 1]) + ht / c * phi[1:I]
            u[k + 1, I] = u[k, I] * (
                        1 - 2 * k_k * ht / c / hx / hx - 2 * alpha * ht / c / R - 2 * alpha * ht / c / hx) + 2 * k_k * ht / c / hx / hx * \
                          u[k, I - 1] + ht / c * phi[I]

    difference_scheme()



    figure = Figure(figsize=(5, 4), dpi=100)
    pl = figure.add_subplot(1, 1, 1)
    pl.grid()

    if not r_var.get():
        u_t0 = u[cut][:]
        pl.plot(z, u_t0)
    elif r_var.get():
        arr = []
        for k in range(K+1):
            arr.append(u[k][cut])
        pl.plot(t, arr)

    canvas = FigureCanvasTkAgg(figure, window)
    canvas.get_tk_widget().grid(row=0, column=0)


window = Tk()
window.geometry('800x660')
x_position = 550

inp_k_k = place_input("k", x_position, 50, '0.59')
inp_alpha = place_input("alpha", x_position, 100, '0.002')
inp_c = place_input("c", x_position, 150, '1.65')
inp_u0 = place_input("u0", x_position, 200, '0')
inp_l = place_input('l', x_position, 250, '8')
inp_S = place_input('S', x_position, 300, '0.01')
inp_T = place_input('T', x_position, 350, '200')
inp_K = place_input('K', x_position, 400, '4000')
inp_I = place_input('I', x_position, 450, '20')
inp_cut = place_input("Координата среза", x_position, 500, '0')

r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(text='Срез по времени', variable=r_var, value=False)
r2 = Radiobutton(text='Срез по координате', variable=r_var, value=True)
r1.place(x=x_position, y=530)
r2.place(x=x_position, y=550)

btn = Button(window, text="Запустить", command=calculate_data)
btn.place(x=x_position, y=600)

window.mainloop()
