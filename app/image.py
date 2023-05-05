import base64
import os
import textwrap
import time

import requests
from PIL import ImageDraw, Image, ImageFont
from dotenv import load_dotenv

from log import logger
from publish import send_image_to_instagram

load_dotenv()

posts_count = 0
instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
access_token = os.getenv("ACCESS_TOKEN")


def upload_image(image):
    url = "https://api.imgur.com/3/image"
    headers = {
        "Authorization": f"Client-ID {os.getenv('IMGUR_CLIENT_ID')}"
    }
    payload = {
        "image": image
    }
    files = []
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()['data']['link']


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
    try:
        global posts_count
        posts_count += 1
        img = Image.new('RGB', (400, 400), (255, 255, 255))
        font = ImageFont.truetype("arial", 24)

        draw_multiple_line_text(img, text, font, (0, 0, 0), 20)

        img.save(f"{os.getcwd()}/image.png")
        time.sleep(3)
        with open("image.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        image_url = upload_image(encoded_string.decode("utf-8"))
        send_image_to_instagram(f"Post numer {posts_count}", image_url, instagram_account_id, access_token)

        return True
    except Exception as er:
        logger.error(er)
        raise er
