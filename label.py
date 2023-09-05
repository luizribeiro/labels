#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import Sequence

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps

WHITE = 1
BLACK = 0

DPI = 180
TAPE_WIDTH = 12 # mm
LABEL_WIDTH = 36 # mm
PADDING = 2 # mm

MAX_HEIGHT = 76 # px (???)

def px(l) -> int:
    return int(DPI * l * 0.03937007874015748)



class Widget(ABC):
    @abstractmethod
    def render(self, draw: ImageDraw.Draw) -> None:
        pass

    def layout(self, width: int, height: int) -> (int, int):
        return (width, height)


class Label(Widget):
    def __init__(self, width: int, height: int, child: Widget) -> None:
        self.width = width
        self.height = height
        self.child = child

    def render(self, draw: ImageDraw.Draw) -> None:
        # markers
        width, height = self.width, self.height
        for x in [0, width-1]:
            for y in range(0, height, 8):
                draw.line([(x, y), (x, y + 4)], fill=BLACK)

        image = Image.new("1", (self.width - 2, self.height), WHITE)
        self.child.render(ImageDraw.Draw(image))

        draw._image.paste(image, (1, 0))


class Horizontal(Widget):
    def __init__(self, children: Sequence[Widget]) -> None:
        self.children = children

    def render(self, draw: ImageDraw.Draw) -> None:
        width, height = draw.im.size

        offered_child_width = int(width / len(self.children))
        spare_width = width
        num_flexible = 0
        for child in self.children:
            desired_width = child.layout(offered_child_width, height)[0]
            if desired_width == offered_child_width:
                num_flexible += 1
            else:
                spare_width -= desired_width
        flexible_child_width = (
            offered_child_width
            if num_flexible == 0
            else int(spare_width / num_flexible)
        )

        x = 0
        for i, child in enumerate(self.children):
            child_layout = child.layout(flexible_child_width, height)
            image = Image.new("1", child_layout, WHITE)
            child.render(ImageDraw.Draw(image))
            draw._image.paste(image, (x, 0))
            x += child_layout[0]


class Vertical(Widget):
    def __init__(self, children: Sequence[Widget]) -> None:
        self.children = children

    def render(self, draw: ImageDraw.Draw) -> None:
        # TODO: this is super basic, need to take into account flexible child
        width, height = draw.im.size

        child_height = int(height / len(self.children))
        for i, child in enumerate(self.children):
            image = Image.new("1", (width, child_height), WHITE)
            child.render(ImageDraw.Draw(image))
            draw._image.paste(image, (0, i * child_height))


class Text(Widget):
    def __init__(self, text: str, size: int = 20) -> None:
        self.text = text
        self.size = size

    def render(self, draw: ImageDraw.Draw) -> None:
        W, H = draw.im.size
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=self.size)
        _, _, w, h = draw.textbbox((0, 0), self.text, font=font)
        draw.text(((W-w)/2, (H-h)/2), self.text, font=font, fill=BLACK)


class QRCode(Widget):
    def __init__(self, data: str) -> None:
        self.data = data

    def render(self, draw: ImageDraw.Draw) -> None:
        width, height = draw.im.size
        qr = qrcode.QRCode(box_size=1)
        qr.add_data(self.data)
        qr.make()
        img_qr = qr.make_image().resize((width, height))
        draw._image.paste(img_qr, (0, 0))

    def layout(self, _width: int, height: int) -> (int, int):
        return (height, height)


label = Label(
    px(LABEL_WIDTH),
    min(px(TAPE_WIDTH), MAX_HEIGHT),
    Horizontal([
        QRCode("sup"),
        Vertical([
            Text("Hello"),
            Text("World"),
        ]),
        QRCode("https://pillow.readthedocs.io/en/latest/reference/Image.html"),
    ]),
)

width, height = px(LABEL_WIDTH + PADDING), min(px(TAPE_WIDTH), MAX_HEIGHT)
image = Image.new("1", (width, height), WHITE)
draw = ImageDraw.Draw(image)
label.render(draw)

image.save("hello_world.png")
