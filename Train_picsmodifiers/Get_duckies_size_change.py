import numpy as np
import cv2
from PIL import Image

# Usar este codigo para cortar las imagenes usando get bbox y crop de pillow (No es necesario cv2)

def pil2cv(pil_img):
    cv_img = np.array(pil_img)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return np.uint8(cv_img)

def cv2pil(cv_img):
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_img)
    return pil_img

cap = cv2.VideoCapture('VID20210612233947.mp4') # Esto lo deberiamos modificar para acceder a una carpeta de imagenes (Estas ya deben de estar en los fondos)

k = 0
while True:
    ret, frame = cap.read()
    if frame is None:
        break

    height, width = frame.shape[:2]
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([50, 0, 0]) # Modificar colores, con tal de identificar cualquier cosa menos blancos
    upper_range = np.array([100, 255, 255]) # ''
    mask = cv2.inRange(frame_hsv, lower_range, upper_range)
    mask = cv2.bitwise_not(mask)

    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask, kernel, iterations = 3) 
    mask = cv2.dilate(mask, kernel, iterations = 3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15,15),np.uint8))
    img_out = cv2.bitwise_and(frame, frame, mask=mask)

    # Definir blobs
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = list()
    rects = list()
    # Dibujar rectangulos de cada blob
    for cnt in contours:
        # Obtener rectangulo que bordea un contorno
        x,y,w,h = cv2.boundingRect(cnt)
        #Filtrar por area minima
        if cv2.contourArea(cnt) > 5000 and cv2.contourArea(cnt) < 80000: 3 # Como proceder con el nuestro?
            x2=x+w
            y2=y+h

            if x < width*0.05 or x2 > width*0.95 or y < height*0.05 or y > height*0.95: # Preguntar por esta parte
                continue
            cnts.append(cnt)
            k += 1
            #Dibujar rectangulo en el frame original
            cv2.rectangle(img_out, (x,y), (x2,y2), (250,0,0), 2)

            rects.append([y-5,y2+5, x-5,x2+5])

    final_mask = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(final_mask, cnts, -1, (255,255,255), -1)
    #for r in rects:
    #    roi = frame[r[0]:r[1], r[2]:r[3]]
    #    mask_roi = final_mask[r[0]:r[1], r[2]:r[3]]
    #    mask_roi = cv2.cvtColor(mask_roi, cv2.COLOR_BGR2GRAY)

    #    pil_img = cv2pil(roi)
    #    pil_mask = Image.fromarray(mask_roi)
    #    pil_img = pil_img.convert('RGBA')
    #    pil_img.putalpha(pil_mask)
    #    pil_img.save('chanchulin/' + str(k).zfill(4) + '.png')


    cv2.imshow('test', img_out)
    key = cv2.waitKey(30)

    if key == ord('q'):
        break

print(k)
