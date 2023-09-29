import cv2
import numpy as np

# Localización de Asientos en el Video
[(110, 940, 70, 40), (120, 830, 50, 70), (465, 740, 40, 65),(530, 740, 50, 80),(610, 770, 50, 60),
              (590, 505, 45, 55),(645, 455, 50, 60),(850, 440, 50, 40),(920, 400, 50, 80),(985, 475, 50, 40),
              (1160, 530, 50, 80),(1220, 580, 50, 80),(1290, 570, 50, 80),(1515, 515, 50, 50),(1700, 430, 60, 45),
              (1340, 290, 50, 60),(1400, 275, 50, 60),(890, 620, 50, 50)]
# Dirección del Video
video = cv2.VideoCapture('video.mp4')

# Estado de Asientos (Libre o Ocupado)
estado_asientos = [False] * len(asientos)

while True:
    check, cuadro = video.read()
    # Convierte la Imagen a Escala de Grises
    cuadroBN = cv2.cvtColor(cuadro, cv2.COLOR_BGR2GRAY)
    # Convertir la Imagen en Escala de Grises a Binaria
    cuadroTH = cv2.adaptiveThreshold(cuadroBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # Reducimos el Ruido de la Imagen
    cuadroMedian = cv2.medianBlur(cuadroTH, 5)
    # Generamos un Área de Detección de 5x5
    kernel = np.ones((5, 5), np.int8)
    # Usamos el Área de Detección como Máscara para Buscar Asientos Ocupados o Libres 
    cuadroDil = cv2.dilate(cuadroMedian, kernel)
    for i, (x, y, w, h) in enumerate(asientos):
        espacio = cuadroDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)
        # Agrega un Indicador "LIBRE" o "OCUPADO" Según el Estado del Asiento
        indicador = "LIBRE" if count < 900 else "OCUPADO"    
        # Escribe el Indicador Encima del Asiento, si es "Libre" se Escribe con Negro
        if indicador == 'LIBRE':
            cv2.putText(cuadro, indicador, (x-7, y - 12), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 2)
        # Escribe el Indicador Encima del Asiento, si es "Ocupado" se Escribe con Rojo
        else:
            cv2.putText(cuadro, indicador, (x-7, y - 12), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
        # Si el Asiento Esta Libre Dibuja el Cuadro
        if count < 900:
            cv2.rectangle(cuadro, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Si el Asiento Esta Ocupado Actutaliza el Asiento Como Ocupado
        else:
            cv2.rectangle(cuadro, (x, y), (x+w, y+h), (255, 0, 0), 2)
            estado_asientos[i] = True
    # Muestra el Video y los Cuadros
    cv2.imshow('video', cuadro)
    # Se Cierra el Programa con la Letra 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
