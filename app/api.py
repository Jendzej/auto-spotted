import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from image import create_image
from log import logger
from mailer import report_error, report_added_post

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/")
async def send_message(body: dict):
    try:
        logger.info(f"Creating post with text: \n {body['message']}")
        response = create_image(body["message"])
        if response:
            report_added_post(body["message"])
        else:
            report_error(response)
        return {
            "status_code": 200,
            "message": "Successfully added post"
        }
    except Exception as er:
        logger.error(er)
        return {
            "status_code": 400,
            "message": er
        }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        reload=True,
        port=8000
    )
