from tkinter import *
import numpy as np

#global ventana, r1, r2, tipoMem, archivoNumero, inputAditivo, inputSustractivo, e5, e6

# Agregar cualquier ruido a imagen
def ruido(img, sal, pimienta):
    alto = img.shape[0]
    ancho = img.shape[1]  
    imgRuido = np.asarray(img.copy(), order = "C")
    dimension = alto*ancho
    # Ruido aditivo, sal
    if sal > 0 and sal <= 1:
        # Número total de pixeles para ruido
        npixels = int(float(dimension) * sal)
        for i in range(npixels):
            x = np.random.randint(0, ancho, 1)
            y = np.random.randint(0, alto, 1)
            # Pixel aleatorio en blanco (255)
            imgRuido[y[0], x[0]] = 255
    # Ruido sustractivo, pimienta
    if pimienta > 0 and pimienta <= 1:
        # Número total de pixeles para ruido
        npixels = int(float(dimension) * pimienta)
        for i in range(npixels):
            x = np.random.randint(0, ancho, 1)
            y = np.random.randint(0, alto, 1)
            # Pixel aleatorio en negro (0)
            imgRuido[y[0], x[0]] = 0
    return imgRuido

# Convertir a escala de grises (0-255)
def escalaGrises(img):
    # Dimensiones
    alto = img.shape[0]
    ancho = img.shape[1]
    canal = np.zeros((alto, ancho))
    for i in range(alto):
        for j in range(ancho):
            canal[i][j] = img[i][j][0]
    return canal.astype(dtype = np.uint8)

# Lista de listas -> Una lista con los valores de las sublistas como elementos
def listInList(lista):
    return [[item] for sublista in lista for item in sublista]

#
# Memorias morfológicas: Fase de aprendizaje
#

# Memoria max M
def maxAprendizaje(x, y):
    # Genera M con ceros
    M = np.zeros((y[0].shape[0], x[0].shape[0]))
    # Por cada dimensión
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): 
            # Genera el máximo inicial de x_i + (-x_i)^t
            max = y[0][i][0] - x[0][j][0]
            for p in range(len(x)):
                # Recorre todos los patrones de x
                if (y[p][i][0] - x[p][j][0]) > max:
                    max = y[p][i][0] - x[p][j][0]
            # Asigna cada máximo para cada elemento de M        
            M[i][j] = max
    return M

# Memoria min W
def minAprendizaje(x, y):
    W = np.zeros((y[0].shape[0], x[0].shape[0]))
    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            # Genera el mínimo inicial de x_i + (-x_i)^t
            min = y[0][i][0] - x[0][j][0]
            # Recorre todos los patrones de x
            for p in range(len(x)):
                if (y[p][i][0] - x[p][j][0]) < min :
                    min = y[p][i][0] - x[p][j][0]
            # Asigna cada min para cada elemento de W
            W[i][j] = min
    return W

#
# Memorias morfológicas: Fase de recuperación
#

# Memoria max M
# Por cada x 
def maxRecuperacion(x, M, yN, cfp):
    # Crea una matriz y llena de ceros con el mismo número de filas que M
    y = np.zeros((M.shape[0],1))
    # Recorre columnas de M
    for i in range(M.shape[0]):
        # Calculo del primer valor mínimo
        min = M[i][0] + x[0][0]
        for j in range(x.shape[0]):
            if (M[i][j] + x[j][0]) < min :
                min = M[i][j] + x[j][0]
        # Se crea matriz columna de recuperación        
        y[i][0] = min
    # Checa si la matriz columna coincide con alguna del CFP
    for i in range(len(cfp)):
        if (y == yN[i]).all():
            return(True, i)
    # Si no, retorna -1
    return(False, -1)

# Memoria min W

def minRecuperacion(x, W, yN, cfp):
    y = np.zeros((W.shape[0],1))
    for i in range(W.shape[0]):
        # Calculo del primer valor máximo
        max = W[i][0] + x[0][0]
        for j in range(x.shape[0]):
            if (W[i][j] + x[j][0]) > max :
                max = W[i][j] + x[j][0]
        # Se crea matriz columna de recuperación        
        y[i][0] = max
    # Checa si la matriz columna coincide con alguna del CFP
    for i in range(len(cfp)):
        if (y == yN[i]).all():
            return(True, i)
    return(False, -1)