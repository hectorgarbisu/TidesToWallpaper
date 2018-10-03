import urllib2
from PIL import Image
import os, random
import matplotlib.pyplot as plt
import ctypes
import tidesFromHarmonics as tides, tidesFromWeb

if __name__ == "__main__":

    # Constants
    SPI_SETDESKWALLPAPER = 20
    IMAGE_FOLDER = 'D:/Pictures/walls'
    IMAGE_OUTPUT_NAME = 'D:/Pictures/walls/edited/edited.png'

    # Get data
    waves = tides.get_current_day_forecast(150)
    current_time_index = tides.get_now_index()

    # Selectiof of a random image from folder
    images_in_folder = [file for file in os.listdir(
        IMAGE_FOLDER) if file.endswith(('.png', '.jpg', '.bmp'))]
    random_image = IMAGE_FOLDER+'/'+random.choice(images_in_folder)

    # Print and save plot
    xs = range(len(waves))
    fig, ax = plt.subplots()
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    cti = current_time_index
    ax.plot(xs, waves, '-', linewidth=5, color='firebrick')
    # 10 points before now and 10 points after now are redrawn with different color
    ax.plot(xs[cti-5:cti+5], waves[cti-5:cti+5], '-', linewidth=5, color='green')
    # the current time is drawn with lime color
    ax.plot(xs[cti], waves[cti], 'd', linewidth=5, color='lime')
    plt.savefig(IMAGE_OUTPUT_NAME, bbox_inches='tight', transparent=True)

    # Join plot and wallpaper
    # Wallpaper preparation
    image = Image.open(random_image)
    wallpaper = image.resize((1920, 1080))
    # Attach plot to image
    plot_image = Image.open(IMAGE_OUTPUT_NAME)
    # Crop to remove the frame
    plot_image = plot_image.crop(
        (20, 20, plot_image.width-20, plot_image.height-20))
    plot_image = plot_image.resize(
        (int(plot_image.width*0.5), int(plot_image.height*0.5)))
    # Position is sligthly (50px) above Bottom right corner
    position = ((wallpaper.width - plot_image.width),
                (wallpaper.height - plot_image.height)-50)
    wallpaper.paste(plot_image, position, plot_image)
    wallpaper.save(IMAGE_OUTPUT_NAME)

    # Set as wallpaper
    ctypes.windll.user32.SystemParametersInfoA(
    SPI_SETDESKWALLPAPER, 0, IMAGE_OUTPUT_NAME, 0)
