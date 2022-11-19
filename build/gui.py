import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import json
import os


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Temporal\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Administrador de procesos")
window.geometry("550x480")
window.configure(bg = "#242222")
style = ttk.Style()

canvas = Canvas(
    window,
    bg = "#242222",
    height = 339,
    width = 550,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    127.0,
    24.0,
    anchor="nw",
    text="Control de Procesos",
    fill="#73DEB1",
    font=("RobotoRoman Regular", 32 * -1)
)
label2 = Canvas(
    window,
    bg = "#242222",
    height = 50,
    width = 240,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
label2.place(x = -80, y = 70)
label2.create_text(
    130.0,
    30.0,
    anchor="nw",
    text="N° Procesos",
    fill="#73DEB1",
    font=("RobotoRoman Regular", 14 * -1)
)

validate_entry = lambda text: text.isdecimal()
entry = ttk.Entry(window,
                  font="RobotoRoman",
                  validate="key",
                  validatecommand=(window.register(validate_entry), "%S")
                  )
entry.place(x = 50, y = 130)

label1 = Canvas(
    window,
    bg = "#242222",
    height = 50,
    width = 200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
label1.place(x = 170, y = 70)
label1.create_text(
    130.0,
    30.0,
    anchor="nw",
    text="Catálogo",
    fill="#73DEB1",
    font=("RobotoRoman Regular", 14 * -1)
)

combo = ttk.Combobox(window,
                     state='readonly',
                     values=["Mayor memoria", "Menor memoria"],
                     font="RobotoRoman",
                     )
combo.set("Seleccionar")
combo.place(x = 300, y = 130)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: mostrarProcesos(),
    relief="flat"
)
button_1.place(
    x=210.0,
    y=180.0,
    width=129.0,
    height=38.305877685546875
)

def capturarProcesos():
    Data = subprocess.check_output(['tasklist'])
    a = str(Data).split("\\r\\n")
    proces = []
    for i in range(5, len(a)):
        tmp = a[i].removesuffix('KB').split()
        if len(tmp) == 5:
            datos = ['-', '-', tmp[1], tmp[0], tmp[2], tmp[3], tmp[4]]
            proces.append(datos)
    return  proces

def cambiar(procesos, p1, p2):
    aux = procesos[p1]
    procesos[p1] = procesos[p2]
    procesos[p2] = aux

def ordenarProcesos(procesos, tipo):
    salida = procesos
    for i in range(len(salida)):
        for j in range(len(salida)):
            d1 = int(salida[i][6].replace(".",""))
            d2 = int(salida[j][6].replace(".", ""))
            if tipo==0 and d1 > d2:
                cambiar(salida, i, j)
            elif tipo==1 and d1 < d2:
                cambiar(salida, i, j)
    return salida

def mostrarProcesos():
    procesosJSON = []
    nproces = int(entry.get())
    cata = combo.current()
    proces = ordenarProcesos(capturarProcesos(), cata)
    treeview.delete(*treeview.get_children())
    for i in range(nproces):
        proces[i][0] = i+1;
        proces[i][1] = f"Catalogo {cata+1}"
        treeview.insert('', i, values=tuple(proces[i]))
        procesosJSON.append({
            "id": f"{proces[i][0]}",
            "catalogo":f"{proces[i][1]}",
            "pid":f"{proces[i][2]}",
            "nombre":f"{proces[i][3]}",
            "usuario":f"{proces[i][4]}",
            "prioridad":f"{proces[i][5]}",
            "memoria":f"{proces[i][6]}"
        })
    DIRECTORIO_BASE = "C:/Temporal/Procesos/procesos.json"
    with open(DIRECTORIO_BASE, 'w') as file:
        json.dump(procesosJSON, file, indent=4)

columnas = ("ID", "Catalogo", "PID", "Nombre", "Usuario", "Prioridad", "Memoria")
treeview = ttk.Treeview(window, height=10, show="headings", columns=columnas)  # tabla
treeview.place(x=20, y=100)
treeview.column("ID", width=30, anchor='center')  # indica una columna, no se muestra
treeview.column("Catalogo", width=80, anchor='center')
treeview.column("PID", width=40, anchor='center')
treeview.column("Nombre", width=80, anchor='center')
treeview.column("Usuario", width=80, anchor='center')
treeview.column("Prioridad", width=80, anchor='center')
treeview.column("Memoria", width=80, anchor='center')

treeview.heading("ID", text="ID")
treeview.heading("Catalogo", text="Catálogo")
treeview.heading("PID", text="PID")
treeview.heading("Nombre", text="Nombre")
treeview.heading("Usuario", text="Usuario")
treeview.heading("Prioridad", text="Prioridad")
treeview.heading("Memoria", text="Memoria")
treeview.pack(side=BOTTOM, pady=20)

window.resizable(False, False)
window.mainloop()
