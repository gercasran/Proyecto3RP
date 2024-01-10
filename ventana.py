from main import *
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
from PIL import ImageTk as imtk
from functools import partial
from pathlib import Path


import numpy as np

def filePicker():
    archivo = fd.askopenfilename(title="Selecciona una imagen", filetypes=[("Imagenes BMP", "*.bmp")])
    archivoNumero.delete(0, 'end')
    archivoNumero.insert(0, archivo)

def pFilePicker():
    # Mostrar el diálogo de selección de archivos
    archivos = fd.askopenfilenames(
        title="Selecciona las imagenes para el CFP",
        filetypes=[("Imagenes BMP", "*.bmp")],
        multiple=True
    )
    # Convertir las rutas a cadenas y devolver la lista
    return [str(Path(path).absolute()) for path in archivos]


def recuperacion(imagenRecuperada, digitos):
    # Getters de los datos para la prueba
    numero = archivoNumero.get()
    tipo = min_max_var.get()
    sal = float(inputAditivo.get())/100
    pimienta = float(inputSustractivo.get())/100

    # Se aplica ruido a la imagen escalada a grises y se convierte a arreglo
    imagen = ruido(escalaGrises(np.asarray(im.open(numero))), sal, pimienta) 
    # Se convierte la imagen en el patrón como vector columna
    patron = np.asarray(listInList(imagen.tolist()))
    
    #Selección de tipo
    if tipo == "max":
        resultado, indice = maxRecuperacion(patron, M, arreglo_y, digitos) # Reconoce para sal
        pass
    else:
        resultado, indice = minRecuperacion(patron, W, arreglo_y, digitos) # Reconoce para pimienta
        pass

    # Recupera la imagen del patrón de prueba desde el arreglo 
    img0 = im.fromarray(imagen)
    img0 = img0.resize((150, 150))
    img0 = imtk.PhotoImage(img0)
    panel = Label(ventana, image = img0)
    panel.image = img0 
    panel.place(x = 150, y = 300)

    # Colocación en UI de la imagen recuperada y su numero
    #imagenRecuperada.set("El dígito es " + str(indice) if resultado else "No reconocido")
    imagenRecuperada.set("Digito reconocido " if resultado else "No reconocido")
    # Si se recupera una imagen del CFP
    if indice != -1:
        # Carga la imagen con el indice del patrón
        imagenNumCFP = digitos[indice]
        imagenNumCFP = np.asarray(im.open(imagenNumCFP))      
        # Recupera la imagen del patrón desde el arreglo
        img1 = im.fromarray(imagenNumCFP)
        img1 = img1.resize((150, 150))
        img1 = imtk.PhotoImage(img1)
        panel1 = Label(ventana, image = img1)
        panel1.image = img1 
        panel1.place(x = 150, y = 550)
    else: # Si no se recupera ninguan imagen
        panel1 = Label(ventana, height = 150, width = 150)
        panel1.place(x = 150, y = 550)

# Genera una lista de tamaño n arreglos de tamaño n con un 1 en el indice i
# EJ: generarCFP(3):
#   [
#   [[1][0][0]]
#   [[0][1][0]]
#   [[0][0][1]]
#  ]

def generarCFP(n):
    arreglo_f = []
    for i in range(n):
        arreglo = np.zeros((n, 1), dtype=np.int32)
        arreglo[i] = 1
        arreglo_f.append(np.asarray(arreglo))
    return arreglo_f

if "__main__"==__name__:
    
    digitos = pFilePicker();
    #digitos = [
    #           "img/cero.bmp",
    #           "img/uno.bmp", "img/dos.bmp",
    #           "img/tres.bmp", "img/cuatro.bmp",
    #           "img/cinco.bmp", "img/seis.bmp", 
    #           "img/siete.bmp", "img/ocho.bmp", "img/nueve.bmp"
    #        ]
    arreglo_x = [np.asarray(listInList(escalaGrises(np.asarray(im.open(numero))).tolist())) for numero in digitos]
    arreglo_y = generarCFP(len(digitos))

    # Fase de aprendizaje
    M = maxAprendizaje(arreglo_x, arreglo_y)   
    W = minAprendizaje(arreglo_x, arreglo_y)

    # Inicialización ventana
    ventana = Tk()
    ventana.title("Comunidad 2 - Reconocimiento de digitos en archivo de imagen")
    ventana.geometry("550x810")
    # Interfaces
    labelImagen = Label(ventana, text = "Imagen (.bmp)")
    labelImagen.place(x = 50, y = 40)
    archivoNumero = Entry(ventana, bd = 1)
    archivoNumero.place(x = 350, y = 40)
    botonSeleccionar = Button(ventana, text="Seleccionar imagen", command=filePicker)
    botonSeleccionar.place(x=200, y=35)

    labelMemoria = Label(ventana, text = "Memoria max/min")
    labelMemoria.place(x = 50, y = 70)
    opcionMemoria = ("min","max")
    min_max_var = StringVar()
    tipoMem = OptionMenu(ventana, min_max_var, "min", "max")
    tipoMem.grid(row=2,column=2)
    min_max_var.set("min")
    tipoMem.place(x = 350, y = 65)

    labelAditivo = Label(ventana, text = "Porcentaje de ruido aditivo")
    labelAditivo.place(x = 50, y = 100)
    inputAditivo = Entry(ventana, bd = 1)
    inputAditivo.place(x = 350, y = 100)

    labelSustractivo = Label(ventana, text = "Porcentaje de ruido sustractivo ")
    labelSustractivo.place(x = 50, y = 130)
    inputSustractivo = Entry(ventana, bd = 1)
    inputSustractivo.place(x = 350, y = 130)

    imagenRecuperada = StringVar()
    recuperar = partial(recuperacion, imagenRecuperada, digitos)
    botonAplicar = Button(ventana, text = "Aplicar ruido y reconocer", command = recuperar)
    botonAplicar.place(x = 200, y = 180)

    labelImgOriginal = Label(ventana, text = "Entrada ")
    labelImgOriginal.place(x = 50, y = 260)

    labelImgRecuperada = Label(ventana, textvariable = imagenRecuperada)
    labelImgRecuperada.place(x = 50, y = 490)

 
    ventana.mainloop()

