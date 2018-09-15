import urllib2
from PIL import Image
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import ctypes
SPI_SETDESKWALLPAPER = 20 

URL = "https://www.tide-forecast.com/tides/Puerto-de-la-Luz-Gran-Canaria-Canary-Islands.js"
IMAGE_FOLDER = 'D:/Pictures/walls'
IMAGE_OUTPUT_NAME = 'D:/Pictures/walls/edited/edited.png'

tides_as_list = urllib2.urlopen(URL).read().translate(None,'[] ;').split('\n')[:200]
tide_by_time = map(lambda x: x.split(',')[2:4], tides_as_list)[1:-2]
images_in_folder = [file for file in os.listdir(IMAGE_FOLDER) if file.endswith(('png','jpg','bmp'))]
random_image = IMAGE_FOLDER+'/'+random.choice(images_in_folder)

# Print plot
ys = [float(y) for _,y in tide_by_time]
xs = range(len(ys))
fig, ax = plt.subplots()
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
ax.plot(xs, ys, 'o', linewidth=5, color='firebrick')
ax.plot(xs[50:70], ys[50:70], 'o', linewidth=5, color='green')
ax.plot(xs[60], ys[60], 'o', linewidth=5, color='lime')
plt.savefig(IMAGE_OUTPUT_NAME, bbox_inches='tight', transparent=True)

#Resize to 1080
image = Image.open(random_image)
wallpaper = image.resize((1920, 1080))

#Attach plot to image
plot_image = Image.open(IMAGE_OUTPUT_NAME)
plot_image = plot_image.crop((20, 20, plot_image.width-20, plot_image.height-20))
plot_image = plot_image.resize((int(plot_image.width*0.5), int(plot_image.height*0.5)))
#Bottom right corner
position = ((wallpaper.width - plot_image.width), (wallpaper.height - plot_image.height)-50)
wallpaper.paste(plot_image, position, plot_image)
wallpaper.save(IMAGE_OUTPUT_NAME)

#Set as wallpaper
ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, IMAGE_OUTPUT_NAME , 0)
