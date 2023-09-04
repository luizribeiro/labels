#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from qrcode import QRCode

WHITE = 1
BLACK = 0

DPI = 180
TAPE_WIDTH = 12 # mm
LABEL_WIDTH = 36 # mm
PADDING = 2 # mm

MAX_HEIGHT = 76 # px (???)

def px(l) -> int:
    return int(DPI * l * 0.03937007874015748)

width, height = px(LABEL_WIDTH + PADDING), min(px(TAPE_WIDTH), MAX_HEIGHT)

image = Image.new("1", (width, height), WHITE)
width = px(LABEL_WIDTH)

draw = ImageDraw.Draw(image)
font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=30)

draw.text((2, 2), "Hello world", font=font, fill=BLACK)

qr = QRCode(box_size=1)
qr.add_data('https://pillow.readthedocs.io/en/latest/reference/Image.html')
qr.make()
img_qr = qr.make_image().resize((height, height))

pos = (width - img_qr.size[0], 0)
image.paste(img_qr, pos)

# markers
for x in [0, width-1]:
    for y in range(0, height, 8):
        draw.line([(x, y), (x, y + 4)], fill=BLACK)

image.save("hello_world.png")
