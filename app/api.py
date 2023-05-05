import uvicorn
from fastapi import FastAPI

from image import create_image
from log import logger
from mailer import report_error, report_added_post

app = FastAPI()


@app.post("/")
async def send_message(body: dict):
    logger.info(f"Creating post with text: \n {body['message']}")
    response = create_image(body["message"])
    if response:
        report_added_post(body["message"])
    else:
        report_error(response)


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        reload=True,
        port=8000
    )
