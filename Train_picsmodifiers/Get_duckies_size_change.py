from PIL import Image
import os

# Usar este codigo para cortar las imagenes usando get bbox y crop de pillow (No es necesario cv2)
obj_dir = '/content/Most-Wanted-/Duckies/i_patitos/' # Nombre de la carpeta donde esten todos los PNG
obj_images = os.listdir(obj_dir)
k = 0
for obj_path in obj_images:
    img = Image.open(os.path.join(obj_dir, obj_path))
    A = img.getbbox()
    img = img.crop(A)
    img.save('/content/Most-Wanted-/Duckies/i_patitos_sin_crop/' + str(k).zfill(4) + '.PNG')
    k+=1


