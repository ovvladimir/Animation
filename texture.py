# https://imagemagick.org/index.php
import os
import math
from PIL import Image


def glue_images(path, line, aligment):
    images = [Image.open(path + os.sep + img) for img in os.listdir(path)]
    widths, heights = zip(*(i.size for i in images))
    list_x, list_y = [], []
    list_w = [*widths]
    new_height = max(heights)
    new_width = sum(widths)
    max_width = math.ceil(new_width / line)

    image = Image.new(
        'RGBA', (max_width if line == 2 else new_width, new_height * line))

    x, y, block = 0, 0, False
    for j, im in enumerate(images):
        if aligment == 'center':
            y = round((new_height - heights[j]) / 2.)
        elif aligment == 'bottom':
            y = new_height - heights[j]
        elif aligment == 'top':
            y = 0
        if (x + widths[j] > max_width or block) and line == 2:
            y += new_height
            if not block:
                x, block = 0, True
        image.paste(im, (x, y))
        list_x.append(x)
        list_y.append(new_height if block else 0)
        x += widths[j]

    dict_texture = {
        f'{path[3:]}': {'x': list_x, 'y': list_y, 'w': list_w, 'h': new_height}
    }
    with open('texture.txt', 'a') as fl:
        fl.write(f'{dict_texture}\n')

    image.save(f'out/{path[3:]}.png')
    # image.show()
    print(dict_texture)


if __name__ == "__main__":
    paths = 'in'
    aligments = ['center', 'bottom', 'top']
    lines = [1, 2]

    with open('texture.txt', 'w') as f:
        f.seek(0)
    for num, folder in enumerate(os.listdir(paths)):
        glue_images(paths + os.sep + folder, lines[num], aligments[num])
