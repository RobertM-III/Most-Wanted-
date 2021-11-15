from PIL import Image
import os
import random

def main(): # Se puede usar un randint para ver si usamos 1 2 3 o 4 patos
    obj_dir = '/content/Most-Wanted-/Duckies/i_patitos_sin_crop/'
    obj_images = os.listdir(obj_dir)

    back_dir = '/content/Most-Wanted-/Duckies/Fondos/'
    back_images = os.listdir(back_dir)

    k = 0
    for obj_path in obj_images:
        aleatorio = random.randint(1,2)
        x_ant = 0
        y_ant = 0
        w_ant = 0.001
        h_ant = 0.001
        for i in range(aleatorio):
            if i == 0:
                img = Image.open(os.path.join(obj_dir, obj_path)) # Se accede a la carpeta de imagenes y se obtienen las imagenes (siempre que el formato sea permitido por pil)
                w_obj, h_obj = img.size
                while True:
                    back_path = random.choice(back_images) # Se selecciona aleatoriamente de entre los fondos virtuales
                    back = Image.open(os.path.join(back_dir, back_path)).convert('RGBA') # Se cambia a RGBA
                    width, height = back.size 
                    if width > 10*w_obj or height > 10*h_obj or 1.25*w_obj > width or 1.25*h_obj > height: # En caso que el ancho del fondo sea 10 veces mas grande al del patito o analogamente con la altura, o que el ancho del objeto sea muy grande relativo al ancho del fondo, analogamente con la altura, se salta el fondo 
                        continue
                    if width * 0.5 > w_obj and height * 0.5 > h_obj: # En caso que se cumpla esta otra condicion, se hace un break con la selección aleatoria tal que se continua con el proceso de aumentar el dataset
                        break
            else:
                obj_path = random.choice(obj_images)
                img = Image.open(os.path.join(obj_dir, obj_path))
                w_obj, h_obj = img.size
            
            if width > 10*w_obj or height > 10*h_obj or 1.25*w_obj > width or 1.25*h_obj > height: # En caso que el ancho del fondo sea 10 veces mas grande al del patito o analogamente con la altura, o que el ancho del objeto sea muy grande relativo al ancho del fondo, analogamente con la altura, se salta la inserción del nuevo patito
                back = back.convert('RGB')
                back.save('/content/Most-Wanted-/Duckies/i_patitos_en_fondos/' + str(k).zfill(4) + '.jpg')
                break
            

            rand_x = random.randint(w_obj//8, width - int(w_obj*1.125)) # Se proporcionan coordenadas aleatorias que cumplan con ciertos requisitos, posibles cambios al rango dependiendo de nosotros
            while rand_x > x_ant and x_ant + w_ant//2 > rand_x and w_obj > w_ant//2:
                rand_x = random.randint(w_obj//8, width - int(w_obj*1.125))
            rand_y = random.randint(h_obj//8, height - int(h_obj*1.125))
            while rand_y > y_ant and y_ant + h_ant//2 > rand_y and h_obj > h_ant//2: # Posibles cambios al rango dependiendo de nosotros
                rand_y = random.randint(w_obj//8, width - int(w_obj*1.125))
            back.paste(img, (rand_x, rand_y), img) # Se juntan patito y fondo
            
            x_ant = rand_x
            y_ant = rand_y
            w_ant = w_obj
            h_ant = h_obj
            
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
            
            if i != aleatorio-1:
                with open('/content/Most-Wanted-/Duckies/labels_sin_aumentacion/' + str(k).zfill(4) + '.txt', 'w') as f:
                    f.write('1 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w_obj) + ' ' + str(h_obj) + '\n')
            else:
                back = back.convert('RGB')
                back.save('/content/Most-Wanted-/Duckies/i_patitos_en_fondos/' + str(k).zfill(4) + '.jpg')
                with open('/content/Most-Wanted-/Duckies/labels_sin_aumentacion/' + str(k).zfill(4) + '.txt', 'a') as f:
                    f.write( '1 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w_obj) + ' ' + str(h_obj))
        k += 1
if __name__ == '__main__':
    main()
