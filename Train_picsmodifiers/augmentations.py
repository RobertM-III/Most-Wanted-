from PIL import Image
import os

# Usar este codigo para hacer las aumentaciones de los patitos pegados en los fondos

obj_dir = '/content/Most-Wanted-/Duckies/i_patitos_en_fondos/' # Nombre de la carpeta donde esten las imagenes sin aumentaciones
obj_images = os.listdir(obj_dir)
k = 0

transformacion = A.Compose([
    A.RandomSnow(snow_point_lower=0.3, snow_point_upper=0.7, brightness_coeff=1, always_apply=False, p=0.2), # Agrega nieve
    A.Blur(blur_limit=7, always_apply=False, p=0.2), # Difuminacion
    A.Downscale(scale_min=0.7, scale_max=1.3, interpolation=0, always_apply=False, p=0.2), # Le baja la calidad a la imagen
    A.GaussNoise(var_limit=(25.0, 35.0), mean=0, per_channel=True, always_apply=False, p=0.2), # Aplica ruido gaussiano, que es como para hacer unos puntitos que dajan mas borrosa la imagen
    A.ColorJitter(brightness=[0.7,1.3], contrast=[0.7,1.3], saturation=[0.7,1.3], hue=0.2, always_apply=False, p=0.2), # Cambia brillo, contraste, saturacion y el tono
    A.RandomFog(fog_coef_lower=0.3, fog_coef_upper=0.3, alpha_coef=0.08, always_apply=False, p=0.2), # Agrega neblina
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), num_shadows_lower=1, num_shadows_upper=2, shadow_dimension=5, always_apply=False, p=0.2), # Agrega sombra
    A.RandomToneCurve(scale=0.1, always_apply=False, p=0.2), # Cambia la razon entre las partes mas clara y mas oscuras de la imagen
    A.ToGray(p=0.1), # Cambia la imagen a escala de grises bajo ciertas condiciones
    A.ToSepia(always_apply=False, p=0.1), # Agrega el filtro sepia, que es como mas blanquecino
]) 

# Aqui le aplicamos la transformacion

for obj_path in obj_images:
    img = Image.open(os.path.join(obj_dir, obj_path)) # Cargamos la imagen y la guardamos en una variable
    transformada = transformacion(image=img) # Le aplicamos la transformacion a la imagen anterior, entrega un diccionario con una unica entrada, que es la imagen
    img_final = transformada["image"] # Extraemos dicha imagen del diccionario
    img_final.save('/content/Most-Wanted-/Duckies/i_patitos_aumentados/' + str(k).zfill(4) + '.jpg') # Guardamos la imagen_final en una carpeta 
    k+=1
