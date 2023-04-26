from PIL import ImageDraw, Image, ImageFont
import os
import textwrap


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=22)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height


def create_image(text):
    img = Image.new('RGB', (400, 400), (255, 255, 255))
    font = ImageFont.truetype("arial", 24)

    draw_multiple_line_text(img, text, font, (0, 0, 0), 20)

    img.save(f"{os.getcwd()}/image.jpg")
