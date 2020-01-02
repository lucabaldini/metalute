import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.io import imread
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

file_path = '/data/projects/metalute/a3_grid.jpg'
dx = 340.
dy = 220.
r1 = 2.
r2 = 8.
data = imread(file_path)

x = np.array([4488, 4488, 472, 472])
y = np.array([3053, 454, 454, 3053])
r = np.array([95, 95, 95, 95])
print(x, y, r)

x0 = x.mean()
y0 = y.mean()
r0 = r.mean()
print(x0, y0, r0)

scale_x = (x.max() - x.min()) / dx
scale_y = (y.max() - y.min()) / dy
scale_r = r0 / r2
scale = 0.5 * (scale_x + scale_y)
print(scale_x, scale_y, scale_r, scale)

rexp = int(r0 * r1 / r2)

# Load picture and detect edges
#image = img_as_ubyte(data.coins()[160:230, 70:270])
#image = img_as_ubyte(data[200:600, 200:600])
image = img_as_ubyte(data)
edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)


# Detect two radii
hough_radii = np.arange(rexp - 1, rexp + 2, 1)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=1000)
print((cx - x0) / scale)
print((cy - y0) / scale)

# Draw them
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
image = color.gray2rgb(image)
for center_y, center_x, radius in zip(cy, cx, radii):
    print(center_y, center_x, radius)
    #circy, circx = circle_perimeter(center_y, center_x, radius,
    #                                shape=image.shape)
    #image[circy, circx] = (220, 20, 20)
    plt.plot([center_x], [center_y], 'o', color='red', markersize=1.5)

ax.imshow(image, cmap=plt.cm.gray)
plt.show()
