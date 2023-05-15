import requests
from dotenv import load_dotenv

from log import logger

load_dotenv()

graph_url = 'https://graph.facebook.com/v16.0/'


def send_image_to_instagram(caption, image_url, instagram_account_id, access_token):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['image_url'] = image_url

    response = requests.post(url, params=param)
    response = response.json()
    if 'error' not in response.keys():
        logger.info("Successfully sent image to instagram.")
        logger.debug(f"Response: {response}")
        publish_image_on_instagram(instagram_account_id, response['id'], access_token)
    else:
        logger.error(f"{response['error']['message']}")


def publish_image_on_instagram(instagram_account_id: str, container_id: str, access_token: str):
    url = graph_url + instagram_account_id + "/media_publish"
    param = {"creation_id": container_id,
             "access_token": access_token}

    response = requests.post(url, params=param)
    response = response.json()
    logger.debug(f"Response: {response}")
    if 'error' not in response.keys():
        logger.info("Successfully published photo on Instagram.")
        return response
    else:
        logger.error(f"{response['error']['message']}")
        raise Exception(response)
