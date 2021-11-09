import cv2
from PIL import Image
import albumentations as A
import os
import random

# Modificar para nuestros archivos

def main(): # Se puede usar un randint para ver si usamos 1 2 3 o 4 patos
    obj_dir = 'chanchulin' # Nombre de la carpeta donde esten todos los PNG
    obj_images = os.listdir(obj_dir)

    back_dir = 'random_backgrounds' # Fondos virtuales random que usaremos
    back_images = os.listdir(back_dir)

    k = 0
    for obj_path in obj_images:
        img1 = Image.open(os.path.join(obj_dir, obj_path)) # Se accede a la carpeta de imagenes y se obtienen las imagenes (siempre que el formato sea permitido por pil)
        img2 = Image.open(random.choice(os.path.join(obj_dir, obj_path))) # Se accede a la carpeta de imagenes y se obtienen las imagenes (siempre que el formato sea permitido por pil)
        img3 = Image.open(random.choice(os.path.join(obj_dir, obj_path))) # Se accede a la carpeta de imagenes y se obtienen las imagenes (siempre que el formato sea permitido por pil)
        img4 = Image.open(random.choice(os.path.join(obj_dir, obj_path))) # Se accede a la carpeta de imagenes y se obtienen las imagenes (siempre que el formato sea permitido por pil)
        mask = img.getchannel('A') # De channel alpha
        w_obj1, h_obj1 = img1.size # Necesariamente se usará el tamaño del patito, pero que ocurre con aquellos patitos que tienen mucho menor tamaño al de la imagen (como los mini keychain)

        while True:
            back_path = random.choice(back_images) # Se selecciona aleatoriamente de entre los fondos virtuales
            back = Image.open(os.path.join(back_dir, back_path)).convert('RGBA') # Se cambia a RGBA
            width, height = back.size 
            if width > 10*w_obj or height > 10*h_obj: # En caso que el ancho del fondo sea 10 veces mas grande al del patito o analogamente con la altura, se salta el fondo 
                continue
            if width * 0.5 > w_obj and height * 0.5 > h_obj: # En caso que se cumpla esta otra condicion, se hace un break con la selección aleatoria tal que se continua con el proceso de aumentar el dataset
                break



        rand_x = random.randint(w_obj//8, width - int(w_obj*1.125)) # Se proporcionan coordenadas aleatorias que cumplan con ciertos requisitos
        rand_y = random.randint(h_obj//8, height - int(h_obj*1.125))

        back.paste(img, (rand_x, rand_y), img) # Se juntan patito y fondo

        if rand_x + w_obj > width:
            w_obj = width - rand_x
        elif rand_x < 0:
            w_obj = rand_x + w_obj
            rand_x = 0
        if rand_y + h_obj > height:
            h_obj = height - rand_y
        elif rand_y < 0:
            h_obj = rand_y + h_obj
            rand_y = 0

        c_x = rand_x + w_obj // 2
        c_y = rand_y + h_obj // 2

        c_x /= width
        c_y /= height

        w_obj /= width
        h_obj /= height

        back = back.convert('RGB')
        back.save('images/' + str(k).zfill(4) + '.jpg')

        with open('labels/' + str(k).zfill(4) + '.txt', 'w') as f:
            f.write('1 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w_obj) + ' ' + str(h_obj))

        k += 1
if __name__ == '__main__':
    main()
