import base64
from pygame import *
import sys

img = image.load("toonie.jpg")

print(img.get_width(), img.get_height())

arrayimage = image.tobytes(img, "RGB")

newimg = image.frombuffer(arrayimage, (1209,1200), "RGB")




with open("text.txt", "w") as f:
    f.write(f"{arrayimage}")


