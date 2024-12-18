from utils import min_rgb_filter
from PIL import Image
img = Image.open('screenshot.png')
img = min_rgb_filter(img)
img.save('a.png')