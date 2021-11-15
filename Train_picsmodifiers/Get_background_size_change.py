from PIL import Image
import os

# Usar este codigo para obtener fondos de 400x400 a partir de fondos de mayor tamaño
obj_dir = '/content/Most-Wanted-/Duckies/Fondos/' # Nombre de la carpeta donde esten todos los fondos
obj_images = os.listdir(obj_dir)
k = 0
for obj_path in obj_images:
    img = Image.open(os.path.join(obj_dir, obj_path)).convert('RGBA')
    width, height = img.size
    if width > 400 and height > 400:
        A = (width//2-200,height//2-200,width//2+200,height//2+200)
        img = img.crop(A)
        img = img.convert('RGB')
        img.save('/content/Most-Wanted-/Duckies/Fondos/' 'z_Fondo_cambiado_n_'+ str(k).zfill(4) + '.jpg')
        k+=1
    if k > 150:
        break


