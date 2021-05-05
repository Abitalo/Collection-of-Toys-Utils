def get_palette_freq(img, topk=16, mask=None):
    if img.mode not in ('RGB','RGBA'):
            print('Illegal mode of image, shall be RGB or RGBA !')
            return None
    
    mat = np.array(img)
    if img.mode == 'RGBA' and mask is None:
        img_quant = mask_quantize(mat[:,:,:3], mat[:,:,3])
    else:
        img_quant = mask_quantize(mat[:,:,:3], mask)
#     print(img_quant.getcolors())

    pairs = enumerate(img_quant.getcolors())
    desc_idxs = [x[0] for x in sorted(pairs, key=lambda x: -x[1][0])]
    
    freqs = np.asarray([x[0] for x in img_quant.getcolors()])
    rgbs = np.reshape(img_quant.getpalette(), (-1, 3))

    topk_freqs =freqs[desc_idxs[:topk]]
    topk_rgbs = rgbs[desc_idxs[:topk]]
    
    return topk_rgbs, topk_freqs

def mask_quantize(mat, mask=None):
    if mask is None:
        img = Image.fromarray(mat)
        img_quant = img.quantize(32,2)
        return img_quant
    
    if mat.shape[:2] != mask.shape[:2]:
        print('dimensions of image and mask does not match!')
        return None
    
    masked_vec = mat[np.where(mask)]
    masked_mat = masked_vec.reshape(1,-1,3)
    img = Image.fromarray(masked_mat)
    img_quant = img.quantize(32,2)
    return img_quant

def freq_bar(colors, freq):
    """ plot a color bar with width correspond to its frequencies.

    Args:
        colors (ndarray<n,3>): RGB triplet, scale from 0-255, uint8 dtype.
        freq (ndarray<n,1>): un-normalized frequencies, count the number of pixels, int16 dtype.

    Returns:
        PIL.PngImagePlugin.PngImageFile: a rendered freq bar PIL image.
    """
    freq = freq / sum(freq)
    canvas = np.zeros((50, 1000, 3), dtype=np.uint8)
    l, r = 0, 0
    for i, f in enumerate(freq):
        l = r
        r += f
        if i != len(freq) - 1:
            canvas[:, int(l * 1000): int(r * 1000), :] = colors[i]
        else:
            canvas[:, int(l * 1000):, :] = colors[i]
    return Image.fromarray(canvas)
