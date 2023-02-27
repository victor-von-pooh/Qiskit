import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

def fractal(c0, c1, height=1000, width=1000, x=0, y=0, zoom=1, max_iterations=100):
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom

    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    z = x + 1j * y

    c0 = np.full(z.shape, c0)
    c1 = np.full(z.shape, c1)

    div_time = np.zeros(z.shape, dtype=int)

    m = np.full(c0.shape, True, dtype=bool) 
    for i in range(max_iterations):
        z[m] = (c0[m] * z[m] ** 2 + 1 - c0[m]) / (c1[m] * z[m] ** 2 + 1 - c1[m])
        m[np.abs(z) > 2] = False 
        div_time[m] = i
    return div_time

def data_import(json_filename):
    all_data = []
    with open(json_filename, 'r') as f:
        data = json.load(f)
        for i in range(1, len(data) + 1):
            all_data.append(data[f'state_{i}'])
    
    info = []
    for i in range(len(all_data)):
        z0 = all_data[i]['|0>']['real'] + all_data[i]['|0>']['imag'] * 1j
        z1 = all_data[i]['|1>']['real'] + all_data[i]['|1>']['imag'] * 1j
        info.append([z0, z1])
    
    return info

info = data_import('dataset.json')

for i in range(240):
    fig, ax = plt.subplots(1, 2, figsize=(20, 20))

    if i + 1 < 100:
        if i + 1 < 10:
            name = f'bloch/circ_00{i + 1}.png'
            savename = f'figures/fig_00{i + 1}.png'
        else:
            name = f'bloch/circ_0{i + 1}.png'
            savename = f'figures/fig_0{i + 1}.png'
    else:
        name = f'bloch/circ_{i + 1}.png'
        savename = f'figures/fig_{i + 1}.png'

    ax[0].imshow(mpimg.imread(name))
    ax[0].axis('off')

    ax[1].imshow(fractal(info[i][0], info[i][1]), cmap='magma')
    ax[1].axis('off')

    plt.savefig(savename)