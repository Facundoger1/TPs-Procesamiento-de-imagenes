###Cargo imagen###
import cv2 as cv
from skimage import color
import numpy as np


def RgbYiqPIXELS(img):
    import numpy as np
    import cv2 as cv

    #img= cv.imread('340.jpg') #leo imagen
    img1=cv.cvtColor(img, cv.COLOR_BGR2RGB) #convierto de BGR a RGB

    ###Genero todos  los ndarray que voy a usar###
    colorRGB_pixel_norm=np.zeros((img1.shape[0], img1.shape[1],img1.shape[2]))
    colorYIQ_pixel_norm=np.zeros((img1.shape[0], img1.shape[1],img1.shape[2]))
    colorYIQ_pixel_norm_mod=np.zeros((img1.shape[0], img1.shape[1],img1.shape[2]))
    colorRGB_pixel_norm2=np.zeros((img1.shape[0], img1.shape[1],img1.shape[2]))
    colorYIQ_pixel_norm_prueba=np.zeros((img1.shape[0], img1.shape[1],img1.shape[2]))
    colorBytes_pixel_norm2=np.zeros((img1.shape[0], img1.shape[1]), dtype=np.uint8)
    ######
    yiq_matriz = np.array([[0.2989, 0.5866, 0.1145],
                [0.5959, -0.2744, -0.3216],
                [0.2115, -0.5227, 0.3112]]) #matriz transformacion RGB -> YIQ
    yiq_matriz_inv=np.linalg.inv(yiq_matriz)      #matriz inversa transformacion Y'I'Q' -> R'G'B'
    luminancia = 1                       #coef mult luminancia
    saturacion = 1                       #coef mult saturacion

    ###Proceso la imagen pixel x pixel###
    for altura in range(img1.shape[0]):
        for ancho in range(img1.shape[1]):
            colorRGB_pixel=img1[altura,ancho] #tomo un pixel
            colorRGB_pixel_norm[altura,ancho]=colorRGB_pixel/255.0001 #normalizado los valores RGB
            colorYIQ_pixel_norm[altura,ancho]=np.dot(yiq_matriz,colorRGB_pixel_norm[altura,ancho]) #producto punto entre matrices para transformar RGB -> YIQ
            #colorYIQ_pixel_norm_prueba[altura,ancho]=np.dot(yiq_matriz_inv,colorYIQ_pixel_norm[altura,ancho])
            colorYIQ_pixel_norm_mod[altura,ancho]=colorYIQ_pixel_norm[altura,ancho]*[luminancia,saturacion,saturacion] #modificacion de los valores YIQ con coef lum y sat YIQ->Y'I'Q'
            if colorYIQ_pixel_norm_mod[altura,ancho,0] > 1:     #verifico que Y'I'Q' no este fuera de rango
                 print("Y'>1")
                 colorYIQ_pixel_norm_mod[altura, ancho,0]=0.9999
            if colorYIQ_pixel_norm_mod[altura,ancho,1] > 0.5957 or colorYIQ_pixel_norm_mod[altura,ancho,1] < -0.5957:
                 print("I'>-0.5957 o I'>0.5957")
            if colorYIQ_pixel_norm_mod[altura,ancho,2] > 0.5226 or colorYIQ_pixel_norm_mod[altura,ancho,2] < -0.5226:
                 print("Q'>-0.5226 o Q'>0.5226")
            colorRGB_pixel_norm2[altura,ancho]=np.dot(yiq_matriz_inv,colorYIQ_pixel_norm_mod[altura,ancho]) #producto punto entre matrices para transformar Y'I'Q' -> R'G'B'
            #colorBytes_pixel_norm2[altura,ancho]=colorRGB_pixel_norm2[altura,ancho].tobytes()

    colorRGB_pixel_norm2=colorRGB_pixel_norm2*255               #desnormalizar
    #colorRGB_pixel_norm2=colorRGB_pixel_norm2.astype(np.uint8)  #pasar los elementos de ndarray a uint8
    #colorRGB_pixel_norm2=cv.cvtColor(colorRGB_pixel_norm2, cv.COLOR_RGB2BGR)    #RGB --> BGR
    #cv.imshow('Imagen', colorRGB_pixel_norm2)   # Mostrar la imagen en una ventana
    #cv.waitKey(0)

    return colorRGB_pixel_norm, colorYIQ_pixel_norm
#a=RgbYiqPIXELS(cv.imread('340.jpg'))
#c=((color.yiq2rgb(a)) *255).astype(np.uint8))
#b=cv.cvtColor((((color.yiq2rgb(a)) *255).astype(np.uint8)), cv.COLOR_RGB2BGR)
#cv.imshow('Imagen', b)   # Mostrar la imagen en una ventana
#cv.waitKey(0)
