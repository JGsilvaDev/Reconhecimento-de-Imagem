import numpy as np
from PIL import Image

def process_image(image_path):
    # Abre a imagem e a converte para tons de cinza
    image = Image.open(image_path).convert('L')
    # Converte a imagem para um array numpy
    array = np.array(image)
    # Normaliza os valores para 0 (sem peça) ou 1 (com peça)
    normalized_array = (array > 128).astype(int)
    return normalized_array

def subtract_images(image1, image2):
    # Subtrai as duas matrizes de imagem
    result = image1 - image2
    # Normaliza os valores para 0 (sem peça) ou 1 (com peça)
    result = (result > 0).astype(int)
    return result

# Exemplo de uso
image1 = process_image('tabuleiro.png')
image2 = process_image('tabuleiro2.png')

# Subtrai as duas imagens
result = subtract_images(image1, image2)

# Exibe a matriz resultante
print(result)
