#!/usr/bin/env python


"""
For the backends that supports draw_image with optional affine
transform (e.g., ps backend), the image of the output should
have its boundary matches the red rectangles.
"""

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

def get_image():
    delta = 0.25
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    Z = Z2-Z1  # difference of Gaussians
    return Z

def imshow_affine(ax, z, *kl, **kwargs):
    im = ax.imshow(z, *kl, **kwargs)
    x1, x2, y1, y2 = im.get_extent()
    im._image_skew_coordinate = (x2, y1)
    return im


if 1:
    ax = plt.subplot(111)
    Z = get_image()
    im = imshow_affine(ax, Z, interpolation='nearest', cmap=cm.jet,
                       origin='lower', extent=[-2, 4, -3, 2])

    trans_data2 = mtransforms.Affine2D().rotate_deg(30) + ax.transData
    im.set_transform(trans_data2)

    # display intended extent of the image
    x1, x2, y1, y2 = im.get_extent()
    x3, y3 = x2, y1

    ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "r--", lw=3,
            transform=trans_data2)

    ax.set_xlim(-3, 5)
    ax.set_ylim(-4, 4)

    plt.savefig("demo_affine_image")