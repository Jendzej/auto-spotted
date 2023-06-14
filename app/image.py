import base64
import datetime
import os
import textwrap
import time

from PIL import Image, ImageFont
from dotenv import load_dotenv
from imagekitio import ImageKit
from pilmoji import Pilmoji

from publish import send_image_to_instagram

load_dotenv()

posts_count = 0
instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
access_token = os.getenv("ACCESS_TOKEN")


def upload_image(image):
    """ Upload image to imagekit and get URL of it """
    try:
        imagekit = ImageKit(
            private_key=f'{os.getenv("IMAGE_KIT_PRIVATE")}=',
            public_key=f'{os.getenv("IMAGE_KIT_PUBLIC")}=',
            url_endpoint=os.getenv("IMAGE_KIT_ENDPOINT")
        )
        upload = imagekit.upload_file(
            file=image,
            file_name=f"image{posts_count}.png",
        )
        return upload.response_metadata.raw['url']
    except Exception as er:
        raise er


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    """ Line wrapping """
    with Pilmoji(image) as pilmoji:
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=27)
        for line in lines:
            line_width, line_height = font.getsize(line)
            pilmoji.text((round((image_width - line_width) / 2), y_text),
                         line, font=font, fill=text_color)
            y_text += line_height


def remove_old_images(current_image_number):
    """ Deleting old images from server """
    try:
        os.remove(f"{os.getcwd()}/images/image{current_image_number - 2}.png")
    except OSError:
        pass


def create_image(text, color, background_color):
    """ Creating image with given text based on base.png """
    base_color = {
        "basic": "base.png",
        "black": "base-black.png",
        "white": "base-white.png",
        "aqua": "base-aqua.png",
        "brown": "base-brown.png",
        "green": "base-green.png",
        "pink": "base-pink.png"
    }
    try:
        global posts_count
        posts_count += 1
        img = Image.open(f"{os.getcwd()}/images/{base_color[background_color]}")
        font = ImageFont.truetype(f"{os.getcwd()}/fonts/NotoSansNandinagari-Regular.ttf", 50, encoding='utf-8')

        draw_multiple_line_text(img, text, font, color, 120)

        img.save(f"{os.getcwd()}/images/image{posts_count}.png")

        remove_old_images(posts_count)

        while not os.path.exists(f"{os.getcwd()}/images/image{posts_count}.png"):
            time.sleep(1)
        with open(f"{os.getcwd()}/images/image{posts_count}.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        image_url = upload_image(encoded_string.decode("utf-8"))
        caption = f'{datetime.datetime.now().strftime("%c")}'
        send_image_to_instagram(caption, image_url, instagram_account_id, access_token)

        return True
    except Exception as er:
        raise er
