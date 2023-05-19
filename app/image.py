import base64
import datetime
import os
import textwrap
import time

import requests
from PIL import Image, ImageFont
from dotenv import load_dotenv
from pilmoji import Pilmoji

from log import logger
from publish import send_image_to_instagram

load_dotenv()

posts_count = 0
instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
access_token = os.getenv("ACCESS_TOKEN")


def upload_image(image):
    try:
        url = "https://api.imgur.com/3/image"
        headers = {
            "Authorization": f"Client-ID {os.getenv('IMGUR_CLIENT_ID')}"
        }
        payload = {
            "image": image
        }
        files = []
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        logger.debug(f"Imgur response: {response}")
        return response.json()['data']['link']
    except Exception as er:
        raise er


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
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
    try:
        os.remove(f"{os.getcwd()}/images/image{current_image_number - 2}.png")
    except OSError:
        pass


def create_image(text):
    try:
        global posts_count
        posts_count += 1
        img = Image.open(f"{os.getcwd()}/images/base.png")
        font = ImageFont.truetype(f"{os.getcwd()}/fonts/NotoSansNandinagari-Regular.ttf", 50, encoding='utf-8')

        draw_multiple_line_text(img, text, font, (255, 255, 255), 120)

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
