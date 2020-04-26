# https://imagemagick.org/index.php
import os
from PIL import Image

aligment = 'bottom'  # or 'center'
path = 'in'
images = [Image.open(path + os.sep + img) for img in os.listdir(path)]

widths, heights = zip(*(i.size for i in images))
print(widths, heights)
new_width = sum(widths)
new_height = max(heights)

image = Image.new('RGBA', (new_width, new_height))
x = 0
for j, im in enumerate(images):
    if aligment == 'center':
        y = (new_height - heights[j]) // 2
    elif aligment == 'bottom':
        y = new_height - heights[j]
    image.paste(im, (x, y))
    x += widths[j]

image.save('out/img.png')
image.show()
