from PIL import Image
import os
import glob

def create_gif(in_dir, out_filename):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*'])))
    imgs = []

    for i in range(len(path_list)):
        img = Image.open(path_list[i])
        imgs.append(img)

    imgs[0].save(out_filename, save_all=True, append_images=imgs[1:], duration=200, loop=0)

create_gif(in_dir='figures', out_filename='fractal_bloch.gif')