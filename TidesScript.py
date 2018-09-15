import urllib2
from PIL import Image
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import ctypes
import time
from shutil import copyfile

## Constants
SPI_SETDESKWALLPAPER = 20 
URL = "https://www.tide-forecast.com/tides/Puerto-de-la-Luz-Gran-Canaria-Canary-Islands.js"
IMAGE_FOLDER = 'D:/Pictures/walls'
IMAGE_OUTPUT_NAME = 'D:/Pictures/walls/edited/edited.png'
CURRENT_TIME = int(time.time())
WINDOWS_WALLPAPER_PATH = os.environ['AppData']+'/Microsoft/Windows/Themes/TranscodedWallpaper'

## Data and files preparation
#split rows and filter
tides_as_list = urllib2.urlopen(URL).read().translate(None,'[] ;').split('\n')[1:150]
#split and filter columns
tide_by_time = [x.split(',')[2:4] for x in tides_as_list]
xs,ys = zip(*[(int(x[0]), float(x[1])) for x in tide_by_time])
#Current time to display with a separate color
current_time_index = next(x[0] for x in enumerate(xs) if x[1] > CURRENT_TIME)
#Selectiof of a random image from folder
images_in_folder = [file for file in os.listdir(IMAGE_FOLDER) if file.endswith(('.png','.jpg','.bmp'))]
random_image = IMAGE_FOLDER+'/'+random.choice(images_in_folder)

## Print and save plot
ys = [float(y) for _,y in tide_by_time]
xs = range(len(ys))
fig, ax = plt.subplots()
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
cti = current_time_index
ax.plot(xs, ys, '-', linewidth=5, color='firebrick')
# 10 points before now and 10 points after now are redrawn with different color
ax.plot(xs[cti-5:cti+5], ys[cti-5:cti+5], '-', linewidth=5, color='green')
# the current time is drawn with lime color
ax.plot(xs[cti], ys[cti], 'd', linewidth=5, color='lime')
plt.savefig(IMAGE_OUTPUT_NAME, bbox_inches='tight', transparent=True)

##Join plot and wallpaper
#Wallpaper preparation
image = Image.open(random_image)
wallpaper = image.resize((1920, 1080))
#Attach plot to image
plot_image = Image.open(IMAGE_OUTPUT_NAME)
#Crop to remove the frame
plot_image = plot_image.crop((20, 20, plot_image.width-20, plot_image.height-20))
plot_image = plot_image.resize((int(plot_image.width*0.5), int(plot_image.height*0.5)))
#Position is sligthly (50px) above Bottom right corner
position = ((wallpaper.width - plot_image.width), (wallpaper.height - plot_image.height)-50)
wallpaper.paste(plot_image, position, plot_image)
wallpaper.save(IMAGE_OUTPUT_NAME)

#Set as wallpaper
copyfile(IMAGE_OUTPUT_NAME, WINDOWS_WALLPAPER_PATH)
ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, IMAGE_OUTPUT_NAME , 0)
