from PIL import Image
import albumentations as A
import numpy as np
import os
import random

# Usar este codigo para hacer las aumentaciones de los patitos pegados en los fondos

obj_dir = '/content/Most-Wanted-/Duckies/i_patitos_en_fondos/' # Nombre de la carpeta donde esten las imagenes sin aumentaciones
obj_images = os.listdir(obj_dir)
obj_dir2 = '/content/Most-Wanted-/Duckies/labels_sin_aumentacion/'
obj_labels = os.listdir(obj_dir)

funciones = [A.RandomSnow(snow_point_lower=0.3, snow_point_upper=0.7, brightness_coeff=1, always_apply=False, p=1), # Agrega nieve
    A.Blur(blur_limit=7, always_apply=False, p=1), # Difuminacion
    A.Downscale(scale_min=0.7, scale_max=0.7, interpolation=0, always_apply=False, p=1), # Le baja la calidad a la imagen
    A.GaussNoise(var_limit=(25.0, 35.0), mean=0, per_channel=True, always_apply=False, p=1), # Aplica ruido gaussiano, que es como para hacer unos puntitos que dajan mas borrosa la imagen
    A.ColorJitter(brightness=[0.7,1.3], contrast=[0.7,1.3], saturation=[0.7,1.3], hue=0.2, always_apply=False, p=1), # Cambia brillo, contraste, saturacion y el tono
    A.RandomFog(fog_coef_lower=0.3, fog_coef_upper=0.3, alpha_coef=0.08, always_apply=False, p=1), # Agrega neblina
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), num_shadows_lower=1, num_shadows_upper=2, shadow_dimension=5, always_apply=False, p=1), # Agrega sombra
    A.RandomToneCurve(scale=0.1, always_apply=False, p=1), # Cambia la razon entre las partes mas clara y mas oscuras de la imagen
    A.ToGray(p=1), # Cambia la imagen a escala de grises bajo ciertas condiciones
    A.ToSepia(always_apply=False, p=1)]
# Aqui le aplicamos la transformacion
k = 0
for obj_path in obj_images:
    img = Image.open(os.path.join(obj_dir, obj_path)) # Cargamos la imagen y la guardamos en una variable
    img = np.array(img) # Lo pasamos a arreglo numpy para que albumentations pueda leer la imagen, si fuera necesario tambien hay que pasarla a RGB
    obj_path = obj_path.rstrip('.jpg')
    obj_path = obj_path + '.txt'
    category_ids = []
    with open(os.path.join(obj_dir2, obj_path)) as f:
        lines = f.readlines()
        l = list()
        for i in lines:
            a = i.lstrip("0 ")
            a = a.split()
            q = 0
            for r in a:
                a[q] = float(r)
                q += 1
            l = l + [a]
            category_ids = category_ids + [0]
    bboxes = np.asarray(l)
    category_ids = np.array(category_ids)
    aleatorio = random.randint(1,3)
    anterior = []
    composición = []
    for i in range(aleatorio):
        rndm = random.randint(0,9)
        while rndm in anterior:
            rndm = random.randint(0,9)
        anterior = anterior + [rndm]
        composición = composición + [funciones[rndm]]
    transformacion = A.Compose(composición,bbox_params=A.BboxParams(format='yolo', label_fields=['category_ids']))
    transformada = transformacion(image=img, bboxes=bboxes, category_ids=category_ids)# Le aplicamos la transformacion a la imagen anterior y a sus bboxes, entrega un diccionario con 2 entradas, que son la imagen y sus bboxes
    img_final = transformada["image"] # Extraemos dicha imagen del diccionario
    img_final = Image.fromarray(img_final) # Le hacemos la transformacion inversa; de array a imagen
    label = transformada["bboxes"]
    img_final.save('/content/Most-Wanted-/Duckies/i_patitos_aumentados/' + 'aug' + str(k).zfill(4) + '.jpg') # Guardamos la imagen_final en una carpeta
    contador = 0
    for i in label:
        c_x = i[0]
        c_y = i[1]
        w_obj = i[2]
        h_obj = i[3]
        if contador == 0:
            with open('/content/Most-Wanted-/Duckies/labels_sin_aumentacion/' + 'aug' + str(k).zfill(4) + '.txt', 'w') as f:
                    f.write('0 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w_obj) + ' ' + str(h_obj) + '\n')
        else:
            with open('/content/Most-Wanted-/Duckies/labels_sin_aumentacion/' + 'aug' + str(k).zfill(4) + '.txt', 'a') as f:
                    f.write( '0 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w_obj) + ' ' + str(h_obj))
        contador += 1
    
    k+=1
