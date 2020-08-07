# -*- coding: utf8 -*-
"""
Автоколлаж фотографий
Версия: 0.1
Автор Иргит В.А.
url: https://github.com/tarbagan/autocollage
"""
import os
from PIL import Image, ImageEnhance
import datetime
import os

folder = r'd:\Python_Progect\autocollage\in_photo'
folder_out = r'd:\Python_Progect\autocollage\out_photo'


width = 3000
init_height = 1000
dpi = 300
margin_size = 5
margin_color = (255, 255, 255)
in_brightness = 1.0
in_contrast = 1.0
in_sharpness = 1.0
in_color = 1.0


def make_collage(images, width, init_height):
    """
    Make a collage image with a width equal to `width` from `images` and save to `filename`.
    """
    if not images:
        print('No images for collage found!')
        return False

    # run until a suitable arrangement of images is found
    while True:
        # copy images to images_list
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 5
        while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            # when `x` will go beyond the `width`, start the next line
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        # finally add the last line with images
        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images
        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            # reduce `init_height`
            init_height -= 10
        else:
            break

    # get output height
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), margin_color)
    # put images to the collage
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)

                brightness = ImageEnhance.Brightness(img)
                img = brightness.enhance(in_brightness)
                contrast = ImageEnhance.Contrast(img)
                img = contrast.enhance(in_contrast)
                sharpness = ImageEnhance.Sharpness( img )
                img = sharpness.enhance(in_sharpness)
                color = ImageEnhance.Color( img )
                img = color.enhance(in_color)

                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size

    now = datetime.datetime.now()
    file_name = now.strftime( "%d%m%Y%H%M%S" )
    output = f'collage_{file_name}.jpg'

    output_itog = f'{folder_out}/{output}'
    collage_image.save(output_itog, dpi=(dpi, dpi))
    return output_itog


files = [f'{folder}\\{x}' for x in os.listdir(folder) if x.split('.')[-1] == 'jpg' or x.split('.')[-1] == 'JPG']
make_collage(files, width, init_height)
