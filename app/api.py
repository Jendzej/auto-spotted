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
    """ Function, that handles requests to API. """
    try:
        with open("banned_words.txt", "r") as f:
            for line in f.readlines():
                if line.strip() in body["message"].replace(" ", "").lower() or len(body["message"]) <= 5:
                    report_error(body["message"])
                    return {
                        "status_code": 422,
                        "message": "Unprocessable entity"
                    }
                else:
                    pass
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
        report_error(er)
        return {
            "status_code": 400,
            "message": str(er)
        }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
