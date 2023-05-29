import cv2 as cv
import numpy as np
from tp1 import RgbYiqPIXELS
from skimage import color
import matplotlib.pyplot as plt

def Crear_Histograma(img_YIQ):
  cantDivHistog=10
  cont=[0]*cantDivHistog
  for altura in range(img_YIQ.shape[0]):
      for ancho in range(img_YIQ.shape[1]):
        for x in range(cantDivHistog):
          if img_YIQ[altura,ancho,0]>=(x/cantDivHistog) and img_YIQ[altura,ancho,0]<((x+1)/cantDivHistog):
            cont[x]=cont[x]+1
        if img_YIQ[altura,ancho,0]>=1:
          cont[cantDivHistog-1]=cont[cantDivHistog-1]+1
  return cont

def Graf_Histograma(cont_lum):
    cont_lum_prom = []
    for valor in cont_lum:
        resultado = valor / sum(cont_lum)
        cont_lum_prom.append(resultado)
    print(cont_lum_prom)

    posiciones = range(len(cont_lum_prom))
    plt.bar(posiciones, cont_lum_prom)
    plt.xlabel('Elementos')
    plt.ylabel('Valores')
    plt.title('Gráfico de Barras')
    plt.show()

def filtro_ilum(img_YIQ):
    filtro_seleccionado = input("Seleccione el tipo de filtro (1: Raiz cuadrada, 2: Potencia cuadrada, 3: Lineal a trozos): ")
    if filtro_seleccionado == "1":
        for altura in range(img_YIQ.shape[0]):
            for ancho in range(img_YIQ.shape[1]):
                img_YIQ[altura, ancho, 0] = img_YIQ[altura, ancho, 0] ** 0.5
    elif filtro_seleccionado == "2":
        for altura in range(img_YIQ.shape[0]):
            for ancho in range(img_YIQ.shape[1]):
                img_YIQ[altura, ancho, 0] = img_YIQ[altura, ancho, 0] ** 2
    elif filtro_seleccionado == "3":
        Ymin, Ymax, pendiente = float(input("Seleccione limite Ymin: ")), float(input("Seleccione limite Ymax: ")), float(input("Pendiente: "))
        for altura in range(img_YIQ.shape[0]):
            for ancho in range(img_YIQ.shape[1]):
                if img_YIQ[altura, ancho, 0]<=Ymin:
                    img_YIQ[altura, ancho, 0]=0
                elif img_YIQ[altura, ancho, 0]>Ymin and img_YIQ[altura, ancho, 0]<Ymax:
                    img_YIQ[altura, ancho, 0]=img_YIQ[altura, ancho, 0]*pendiente
                    if img_YIQ[altura, ancho, 0]>1:
                        img_YIQ[altura, ancho, 0]=1
                elif img_YIQ[altura, ancho, 0]>Ymax:
                    img_YIQ[altura, ancho, 0]=1
    else:
        print("Opción inválida. Seleccione 1, 2 o 3.")
    return img_YIQ

_, img_YIQ_340 = RgbYiqPIXELS(cv.imread('chanchi.jpeg'))
#ll=img_YIQ_340.copy()
img_YIQ_filtro=filtro_ilum(img_YIQ_340)
#img_YIQ_filtro=img_YIQ_340
cont_340=Crear_Histograma(img_YIQ_filtro)
Graf_Histograma(cont_340)

#YIQ->BGR
img_BGR_filtro=cv.cvtColor((((color.yiq2rgb(img_YIQ_filtro)) *255).astype(np.uint8)), cv.COLOR_RGB2BGR)
# Mostrar la imagen con filtro
cv.imshow("Imagen", img_BGR_filtro)
cv.waitKey(0)
cv.destroyAllWindows()