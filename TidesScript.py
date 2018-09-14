import urllib2
import time
from PIL import Image
import os
import random

URL = "https://www.tide-forecast.com/tides/Puerto-de-la-Luz-Gran-Canaria-Canary-Islands.js"
CURRENT_TIME = time.time()
IMAGE_FOLDER = 'D:/Pictures/walls'
IMAGE_OUTPUT_NAME = 'D:/Desktop/test_image.png'

tides_as_list = urllib2.urlopen(URL).read().translate(None,'[] ;').split('\n')
tide_by_time = dict(map(lambda x: x.split(',')[2:4], tides_as_list)[1:-2])
images_in_folder = [file for file in os.listdir(IMAGE_FOLDER) if file.endswith(('png','jpg','bmp'))]
image = Image.open(IMAGE_FOLDER+'/'+random.choice(images_in_folder))

# Image resize test
new_image = image.resize((50, 50))
new_image.save(IMAGE_OUTPUT_NAME)

print(image.size) # Output: (1200, 776)
print(new_image.size) # Output: (400, 400)