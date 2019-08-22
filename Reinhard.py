# -*- coding: utf-8 -*-
"""
Created on Tue May 6 16:33:55 2019

@author: 19038067
"""
import numpy as np
import cv2
from matplotlib.colors import hex2color
from skimage import color

# 构建reference图片的噪声的部分
def _make_noisy_ref(src, hex):
    src_gray = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    src_gray = cv2.resize(src_gray, (100, 100), interpolation=cv2.INTER_AREA)
    c_map = (src_gray - src_gray.mean()) / src_gray.std()

    rgb_pix = hex2color(hex)

    # 完成涂色
    im_tar = np.ones((100, 100, 3), dtype=np.float)
    for i in range(3):
        im_tar[:, :, i] = rgb_pix[i]

    # 加扰动，这一块纯经验值，可以看心情改
    im_tar = color.rgb2hsv(im_tar)
    if 0.45 < im_tar[0, 0, 0] < 0.55:       # 浅蓝色单独处理
        im_tar[:, :, 2] += c_map * 0.06
    elif im_tar[0, 0, 1] > 0.95:    # S>0.95
        im_tar[:, :, 2] += c_map * 0.05     # 亮度加扰动
    elif im_tar[0, 0, 1] > 0.9:     # 0.95>S>0.9
        im_tar[:, :, 2] += c_map * 0.002    # 亮度加扰动
    elif im_tar[0, 0, 1] > 0.8:     # 0.9 >S >0.8
        im_tar[:, :, 1] += c_map * 0.06     # 饱和度加扰动
    else:                           # S<0.8
        im_tar[:, :, 1] += c_map * 0.08     # 饱和度加扰动

    im_tar = np.uint8(color.hsv2rgb(im_tar) * 255)
    return im_tar


# Reinhard的目标颜色版本
def Reinhard(img, hex):
    image = cv2.imdecode(np.fromfile(src, dtype=np.uint8), -1)
    if image.shape[-1] == 4:
        alpha = image[:, :, 3:]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
#     alpha = np.reshape(image[:,:,-1], (image.shape[0],-1,1))
    original = _make_noisy_ref(src, hex)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2LAB)

    image_avg, image_std = np.mean(image,(0,1)), np.std(image,(0,1))
    original_avg, original_std = np.mean(original,(0,1)), np.std(original,(0,1))
    
    image = (image-image_avg)*(original_std/image_std)+(original_avg)
    image = np.where(image>255,255,image)
    image = np.where(image<0, 0, image)
    image = image.astype(np.uint8)
    
    image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
    
    if alpha is not None:
        image = np.concatenate([image, alpha], -1)
    return image

if __name__ == '__main__':
    img = Image.fromarray(Reinhard('orignial.png','#f1f2f3'))
    img.save('Reinhard.png')