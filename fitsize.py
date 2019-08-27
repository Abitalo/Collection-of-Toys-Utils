from PIL import Image

# resize PIL with only 1 dim specified.
def fitsize(img, size):
    assert size and len(size) == 2, '"size" must in 2-dim'
    assert (size[0]==-1 and size[1] > 0) or (size[0] > 0 and size[1]==-1), 'at least 1 dimension in "size" be -1'
    w, h = img.size
    if size[0] > 0:
        new_h = int((size[0]/w)*h)
        img = img.resize((size[0], new_h), Image.CUBIC)
    else:  # size[1]>0
        new_w = int((size[1]/h)*w)
        img = img.resize((new_w, size[1]), Image.CUBIC)
    return img