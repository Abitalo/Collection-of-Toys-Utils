import numpy as np
from PIL import Image


# theme color extraction works for image with alpha channel by drop all transparent pixcel.
def get_theme_color(img, quantize_size=10, quantize_algo=2):
    if img.mode == 'RGB':
        return img.quantize(quantize_size, quantize_algo).getpalette()[:3]
    if img.mode == 'RGBA':
        img_arr = np.asarray(img)
        alpha = img_arr[:, :, -1]
        mask = np.where(alpha == 0, False, True)
        palette = Image.fromarray(img_arr[mask].reshape(
            1, -1, 4)).quantize(quantize_size, quantize_algo).getpalette()

        return palette[:3]
