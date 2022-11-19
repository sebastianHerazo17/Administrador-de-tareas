import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import json
import os
import time
from shutil import rmtree


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Temporal\build\assets\frame0")
DIRECTORIO_BASE = "C:/Temporal/Procesos/procesos.json"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title("Administrador de procesos")
window.geometry("550x600")
window.configure(bg = "#242222")

canvas = Canvas(
    window,
    bg = "#242222",
    height = 339,
    width = 550,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
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
entry4 = ttk.Entry(window,
                  font="RobotoRoman",
                  validate="key"
                  )
entry4.place(x = 50, y = 160)

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

canvas.place(x = 0, y = 0)
canvas.create_text(
    127.0,
    24.0,
    anchor="nw",
    text="Control de Procesos",
    fill="#73DEB1",
    font=("RobotoRoman Regular", 32 * -1)
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
    background= "#242222",
    command=lambda: mostrarProcesos(),
    relief="flat"
)
button_1.place(
    x=300.0,
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

proces = []
simular = 0

def mostrarProcesos():
    procesosJSON = []
    if os.path.exists('procesos'):
        rmtree('procesos')
    os.mkdir('procesos')
    nproces = int(entry.get())
    cata = combo.current()
    proces = ordenarProcesos(capturarProcesos(), cata)
    treeview.delete(*treeview.get_children())
    for i in range(nproces):
        proces[i][0] = i+1
        proces[i][1] = f"Catalogo {cata+1}"
        treeview.insert('', i, values=tuple(proces[i]))
        procesosJSON.append({
            "id": f"{proces[i][0]}",
            "catalogo":f"{proces[i][1]}",
            "pid":f"{proces[i][2]}",
            "nombre":f"{proces[i][3]}",
            "usuario":f"{proces[i][4]}",
            "prioridad":f"{proces[i][5]}",
            "memoria":f"{proces[i][6]}",
            "iteraciones": 0,
            "tiempoLlegada": -1,
            "tiempoFin": 0,
            "restante": 0,
            "estado": "Esperando"
        })
    with open(DIRECTORIO_BASE, 'w') as file:
        json.dump(procesosJSON, file, indent=4)

    nombreNuevo = f"C:/Temporal/Procesos/,{entry4.get()}"

    os.rename(DIRECTORIO_BASE, nombreNuevo)

def delay():
    time.sleep(0.5)

def simularProcesos():
    finalizados = []
    espera = []
    quantum = int(entry2.get())
    with open(DIRECTORIO_BASE) as file:
        espera = json.load(file)
    tiempo = 0
    i = 0
    while len(espera)>0:
        borrar = False
        espera[i]["iteraciones"] = 0 if espera[i]["iteraciones"] == 0 else espera[i]["iteraciones"]
        espera[i]["tiempoLlegada"] = tiempo if espera[i]["tiempoLlegada"] == -1 else espera[i]["tiempoLlegada"]
        espera[i]["estado"] = "Ejecutandose"
        p = [*espera[i].values()]
        if p[5]=="2" or p[5]=="1":
            for ltr in p[3]:
                tiempo += 1
                escribirLetra(p[3], ltr)
            espera[i]["tiempoFin"] = tiempo #tiempo finalización
            espera[i]["iteraciones"] += 1
            espera[i]["estado"] = "Finalizado"
            finalizados.append(espera[i])
        elif p[5]=="0":
            for n in range(quantum):
                tiempo += 1
                if len(p[3])>0:
                    if p[7] == 0:
                        escribirLetra(p[3], p[3][n])
                    else:
                        j = n + (quantum*p[7])
                        if len(p[3])==j:
                            espera[i]["tiempoFin"] = tiempo  # tiempo finalización
                            espera[i]["estado"] = "Finalizado"
                            finalizados.append(espera[i])
                            borrar = True
                            break
                        elif len(p[3])>j:
                            escribirLetra(p[3], p[3][j])
            if not(borrar):
                espera[i]["iteraciones"] += 1
                espera[i]["estado"] = "Esperando"
                espera.append(espera[i])
        espera.pop(i)
    treeview2.delete(*treeview2.get_children())
    for lista in finalizados:
        treeview2.insert('', i, values=tuple([lista["pid"], lista["nombre"], lista["iteraciones"], lista["tiempoLlegada"], lista["tiempoFin"], lista["estado"]]))
        i+=1



def escribirLetra(name, ltr):
    with open(f'procesos/{name}.txt', 'a') as file:
        file.write(ltr)
        file.close()

columnas = ("ID", "Catalogo", "PID", "Nombre", "Usuario", "Prioridad", "Memoria")
treeview = ttk.Treeview(window, height=6, show="headings", columns=columnas)  # tabla
treeview.place(x=60, y=100)
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
treeview.pack(side=BOTTOM, pady=230)

label3 = Canvas(
    window,
    bg = "#242222",
    height = 40,
    width = 150,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
label3.place(x = 40, y = 180)
label3.create_text(
    30.0,
    20.0,
    anchor="center",
    text="Quantum:",
    fill="#73DEB1",
    font=("RobotoRoman Regular", 14 * -1)
)

entry2 = ttk.Entry(window,
                  font="RobotoRoman",
                   width=5,
                  validate="key",
                  validatecommand=(window.register(validate_entry), "%S")
                  )
entry2.place(x = 110, y = 188)

button_image_2 = PhotoImage(
    file=relative_to_assets("simulador.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    background= "#242222",
    highlightthickness=0,
    command=lambda: simularProcesos(),
    relief="flat"
)
button_2.place(
    x=210.0,
    y=380.0,
    width=129.0,
    height=38.305877685546875
)


columnas = ("PID", "Nombre", "Iteraciones", "tiempoLlegada", "tiempoFin","Estado")
treeview2 = ttk.Treeview(window, height=6, show="headings", columns=columnas)  # tabla
treeview2.place(x=40, y=430)
treeview2.column("PID", width=40, anchor='center')
treeview2.column("Nombre", width=110, anchor='center')
treeview2.column("Iteraciones", width=80, anchor='center')
treeview2.column("tiempoLlegada", width=80, anchor='center')
treeview2.column("tiempoFin", width=80, anchor='center')
treeview2.column("Estado", width=80, anchor='center')
treeview2.heading("PID", text="PID")
treeview2.heading("Nombre", text="Nombre")
treeview2.heading("Iteraciones", text="Iteraciones")
treeview2.heading("tiempoLlegada", text="tLlegada")
treeview2.heading("tiempoFin", text="tFinal")
treeview2.heading("Estado", text="Estado")

#window.resizable(False, False)
window.mainloop()