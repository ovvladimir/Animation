# https://imagemagick.org/index.php
import sys
import os
from PIL import Image


def append_images(images, aligment='bottom'):

    widths, heights = zip(*(i.size for i in images))
    print(widths, heights)

    new_width = sum(widths)
    new_height = max(heights)

    new_im = Image.new('RGBA', (new_width, new_height))

    x = 0
    for j, im in enumerate(images):
        if aligment == 'center':
            y = (new_height - heights[j]) // 2
        elif aligment == 'bottom':
            y = new_height - heights[j]
        new_im.paste(im, (x, y))
        x += widths[j]

    return new_im


path = 'in'
images = [Image.open(path + os.sep + img) for img in os.listdir(path)]
image = append_images(images)
image.save('out/img.png')
image.show()
sys.exit(0)
